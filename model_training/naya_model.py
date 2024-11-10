import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.models import resnet50, ResNet50_Weights
from tqdm import tqdm
from dataset_banao_script import data_ka_loader_banao
import os
from datetime import datetime
import wandb
os.environ["TORCH_HOME"] = "./torch_cache"

class RukJaoBhai:
    def __init__(self, kitna_wait_kare=7, sabse_kam_antar=0):
        self.sabr, self.kitna_farak, self.kitni_baar, self.best_wala_loss, self.jaldi_stop =  kitna_wait_kare, sabse_kam_antar, 0, None, False
    def __call__(self, abhi_wala_loss):
        if not self.best_wala_loss: self.best_wala_loss = abhi_wala_loss
        elif abhi_wala_loss > self.best_wala_loss + self.kitna_farak:
            self.kitni_baar += 1
            if self.kitni_baar >= self.sabr:
                self.jaldi_stop = True
        else:
            self.best_wala_loss = abhi_wala_loss
            self.kitni_baar = 0
def model_ko_save_karo(neural_net, optimizer, kitni_baar_chala, validation_kitna_sahi, 
    kitna_loss, kaha_save_kare, best_hai_kya=False):
    """Bachao model ko"""
    filename = f"best_model_acc{validation_kitna_sahi:.2f}_epoch{kitni_baar_chala}.pth" if best_hai_kya else f"checkpoint_epoch{kitni_baar_chala}_acc{validation_kitna_sahi:.2f}_loss{kitna_loss:.4f}.pth"
    rasta = os.path.join(kaha_save_kare, filename)
    checkpoint = {"epoch": kitni_baar_chala, "model_state_dict": neural_net.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(), "val_acc": validation_kitna_sahi,
        "val_loss": kitna_loss}
    torch.save(checkpoint, rasta); wandb.save(rasta); return rasta
def model_banao(kitne_class, freeze_karna_hai=True):
    os.makedirs("./torch_cache", exist_ok=True)
    neural_net = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    if freeze_karna_hai:
        for param in neural_net.parameters(): param.requires_grad = False
    neural_net.fc = nn.Sequential(nn.Dropout(p=0.3), nn.Linear(neural_net.fc.in_features, 512),
        nn.ReLU(), nn.Dropout(p=0.2), nn.Linear(512, kitne_class))
    for param in neural_net.fc.parameters(): param.requires_grad = True
    return neural_net
def layer_ko_kholo(neural_net, konsa_layer):
    """Layer ko unfreeze karo"""
    if hasattr(neural_net, konsa_layer):
        for param in getattr(neural_net, konsa_layer).parameters(): param.requires_grad = True
        print(f"Layer khol diya: {konsa_layer}")

def ek_baar_sikhao(neural_net, padhai_ka_data, galti_check, optimizer, device, kitna_clip=1.0,):
    neural_net.train()
    abhi_tak_ka_loss = 0.0
    kitna_sahi = 0
    total_data = 0
    loading_bar = tqdm(padhai_ka_data, desc="Padhai Ho Rahi Hai")
    for photo, sahi_jawab in loading_bar:
        photo, sahi_jawab = photo.to(device), sahi_jawab.to(device)
        optimizer.zero_grad()
        model_ka_jawab = neural_net(photo)
        galti = galti_check(model_ka_jawab, sahi_jawab)
        galti.backward()
        torch.nn.utils.clip_grad_norm_(neural_net.parameters(), kitna_clip)
        optimizer.step()
        abhi_tak_ka_loss += galti.item()
        _, hamara_jawab = model_ka_jawab.max(1)
        total_data += sahi_jawab.size(0)
        kitna_sahi += hamara_jawab.eq(sahi_jawab).sum().item()
        loading_bar.set_postfix({"kitna_galti": abhi_tak_ka_loss / total_data,"kitna_sahi_hai": 100.0 * kitna_sahi / total_data})
    return abhi_tak_ka_loss / len(padhai_ka_data), 100.0 * kitna_sahi / total_data

def jaanch_karo(neural_net, test_ka_data, galti_check, device):
    neural_net.eval()
    test_ka_loss = 0.0
    kitna_sahi = 0
    total_data = 0
    with torch.no_grad():
        for photo, sahi_jawab in tqdm(test_ka_data, desc="Jaanch Ho Rahi Hai"):
            photo, sahi_jawab = photo.to(device), sahi_jawab.to(device)
            model_ka_jawab = neural_net(photo)
            galti = galti_check(model_ka_jawab, sahi_jawab)
            test_ka_loss += galti.item()
            _, hamara_jawab = model_ka_jawab.max(1)
            total_data += sahi_jawab.size(0)
            kitna_sahi += hamara_jawab.eq(sahi_jawab).sum().item()
    return test_ka_loss / len(test_ka_data), 100.0 * kitna_sahi / total_data
def main():
    wandb.init(project="inaturalist-classification", name="resnet50-finetune-updated",
        config={"architecture": "ResNet50", "dataset": "iNaturalist", "epochs": 100,
        "batch_size": 32, "initial_lr": 1e-3, "optimizer": "AdamW",
        "scheduler": "ReduceLROnPlateau", "weight_decay": 1e-5, "dropout_rate": 0.5,
        "early_stopping_patience": 7, "grad_clip": 1.0})
    data_ka_folder = "dataset/updated_inaturalist"
    kitni_baar_chalana = wandb.config.epochs
    ek_baar_kitna_data = wandb.config.batch_size
    shuruwati_learning = wandb.config.initial_lr
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_folder = f"outputs/run_{time_stamp}"
    os.makedirs(result_folder, exist_ok=True)
    padhai_data, jaanch_data, kitne_class = data_ka_loader_banao(data_ka_folder, ek_baar_kitna_data)
    print(f"Kitne class hain: {kitne_class}")
    wandb.config.update({"kitne_class": kitne_class})
    neural_net = model_banao(kitne_class, freeze_karna_hai=True)
    neural_net = neural_net.to(device)
    wandb.watch(neural_net, log="all")
    galti_check = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = optim.AdamW(neural_net.parameters(), lr=shuruwati_learning,
        weight_decay=wandb.config.weight_decay)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min",
        factor=0.5, patience=3, verbose=True, min_lr=1e-6)
    jaldi_rokna = RukJaoBhai(kitna_wait_kare=wandb.config.early_stopping_patience)
    best_kitna_sahi = 0.0
    sabse_ache_models = []
    layer_ke_groups = ["layer4", "layer3", "layer2", "layer1"]
    kab_khulega = kitni_baar_chalana // (len(layer_ke_groups) + 1)
    for kitni_baar in range(kitni_baar_chalana):
        print(f"\nBaar number {kitni_baar+1}/{kitni_baar_chalana}")
        if kitni_baar > 0 and kitni_baar % kab_khulega == 0:
            konsa_layer = (kitni_baar // kab_khulega) - 1
            if konsa_layer < len(layer_ke_groups):
                layer_ko_kholo(neural_net, layer_ke_groups[konsa_layer])
                for param_group in optimizer.param_groups:
                    param_group["lr"] = shuruwati_learning * 0.1
        train_galti, train_sahi = ek_baar_sikhao(neural_net, padhai_data, galti_check,
            optimizer, device, wandb.config.grad_clip)
        test_galti, test_sahi = jaanch_karo(neural_net, jaanch_data, galti_check, device)
        jaldi_rokna(test_galti)
        wandb.log({"kitni_baar": kitni_baar + 1, "padhai_galti": train_galti,
            "padhai_kitna_sahi": train_sahi, "test_galti": test_galti,
            "test_kitna_sahi": test_sahi,
            "learning_rate": optimizer.param_groups[0]["lr"]})
        print(f"Padhai mein galti: {train_galti:.4f} Padhai mein sahi: {train_sahi:.2f}%")
        print(f"Test mein galti: {test_galti:.4f} Test mein sahi: {test_sahi:.2f}%")
        if (kitni_baar + 1) % 5 == 0:
            model_ka_rasta = model_ko_save_karo(neural_net, optimizer, kitni_baar,
                test_sahi, test_galti, result_folder, best_hai_kya=False)
            print(f"Model save ho gaya: {model_ka_rasta}")
        if test_sahi > best_kitna_sahi:
            best_kitna_sahi = test_sahi
            best_model_ka_rasta = model_ko_save_karo(neural_net, optimizer, kitni_baar,
                test_sahi, test_galti, result_folder, best_hai_kya=True)
            sabse_ache_models.append({"rasta": best_model_ka_rasta, "baar": kitni_baar,
                "kitna_sahi": test_sahi, "galti": test_galti})
            print(f"Naya best model save hua: {best_model_ka_rasta}")
            if len(sabse_ache_models) > 3:
                purana_model = sabse_ache_models.pop(0)
                if os.path.exists(purana_model["rasta"]):
                    os.remove(purana_model["rasta"])
                    print(f"Purana best model hata diya: {purana_model['rasta']}")
        scheduler.step(test_galti)
        if jaldi_rokna.jaldi_stop:
            print("Jaldi rok diya!")
            break
    print("\nBest models ka summary:")
    for i, model_info in enumerate(sabse_ache_models, 1):
        print(f"{i}. Baar {model_info['baar']}: Sahi={model_info['kitna_sahi']:.2f}%, Galti={model_info['galti']:.4f}")
        print(f"   Rasta: {model_info['rasta']}")
    print(f"Sabse best validation accuracy: {best_kitna_sahi:.2f}%")
    wandb.finish()

if __name__ ==                                                                "__main__": main()
