from dataset_banao_script import data_ka_loader_banao
import torch

def dataloader_test_karo():
    jagah_root = "./dataset/updated_animals"
    prashikshan_loader,jaanch_loader,kitni_class=data_ka_loader_banao(jagah_root,batch_aakar=4)
    print(f"Kitni class hai:{kitni_class}")
    print(f"Kitne prashikshan batch hai:{len(prashikshan_loader)}")
    print(f"Kitne jaanch batch hai:{len(jaanch_loader)}")
    chhavi, kaksha=next(iter(prashikshan_loader))
    print(f"\nEk batch ki shape:")
    print(f"chhavi shape:{chhavi.shape}")
    print(f"kaksha shape:{kaksha.shape}")
    print(f"kaksha:{kaksha}")
    print(f"\nCUDA updabdh hai:{torch.cuda.is_available()}")
    if torch.cuda.is_available(): print(f"GPU device:{torch.cuda.get_device_name(0)}")

if __name__ == "__main__":
    dataloader_test_karo()
