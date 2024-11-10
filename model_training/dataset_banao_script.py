from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import os

class JanwarDataset(Dataset):
    def __init__(self, root_jagah, tabdili=None, vibhajan="train"):
        self.jagah_root = os.path.join(root_jagah, vibhajan)
        self.tabdili = tabdili
        self.shreni = sorted(os.listdir(self.jagah_root))
        self.shreni_se_number = {naam_shreni: number for number, naam_shreni in enumerate(self.shreni)}
        self.tasveerein = []
        self.labels_list = []
        for naam_shreni in self.shreni:
            shreni_folder = os.path.join(self.jagah_root, naam_shreni)
            for tasveer_naam in os.listdir(shreni_folder):
                self.tasveerein.append(os.path.join(shreni_folder, tasveer_naam))
                self.labels_list.append(self.shreni_se_number[naam_shreni])
    def __len__(self):
        return len(self.tasveerein)
    def __getitem__(self, kramank):
        rasta_tasveer = self.tasveerein[kramank]
        chitram = Image.open(rasta_tasveer).convert("RGB")
        label = self.labels_list[kramank]
        if self.tabdili:
            chitram = self.tabdili(chitram)
        return chitram, label
def data_ka_loader_banao(data_jagah, batch_aakar=32, workers_ki_sankhya=4):
    jaanch_tabdili = transforms.Compose([transforms.Resize(224),transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])  # jaanch=validation
    prashikshan_tabdili = transforms.Compose([transforms.RandomResizedCrop(224),transforms.RandomHorizontalFlip(),transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),transforms.RandomRotation(10),transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    prashikshan_data = JanwarDataset(data_jagah, tabdili=prashikshan_tabdili, vibhajan="train")
    jaanch_data = JanwarDataset(data_jagah, tabdili=jaanch_tabdili, vibhajan="val")
    prashikshan_loader = DataLoader(prashikshan_data,batch_size=batch_aakar,shuffle=True,num_workers=workers_ki_sankhya,pin_memory=True,)
    jaanch_loader = DataLoader(jaanch_data,batch_size=batch_aakar,shuffle=False,num_workers=workers_ki_sankhya,pin_memory=True,)
    return prashikshan_loader, jaanch_loader, len(prashikshan_data.shreni)
