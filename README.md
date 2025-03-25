# Marine Detect 🌊🐟

This repository provides access to two **YOLOv8 object detection models** for identifying **species** of interest in **underwater environments**.


## 🐟 Species Scope

The *Fish and Invertebrates* Object Detection Model detects the *Fish and Invertebrates Species* and the *MegaFauna* Object Detection Model detects *MegaFauna and Rare Species*.

- **MegaFauna and Rare Species**: Sharks, Sea Turtles, Rays.
- **Fish Species**: Butterfly Fish (Chaetodontidae), Grouper (Serranidae), Parrotfish (Scaridae), Snapper (Lutjanidae), Moray Eel (Muraenidae), Sweet Lips (Haemulidae), Barramundi Cod (Cromileptes altivelis), Humphead (Napoleon) Wrasse (Cheilinus undulatus), Bumphead Parrotfish (Bolbometopon muricatum), Fish (other than above or unrecognizable).
- **Invertebrates Species**: Giant Clam, Urchin, Sea Cucumber, Lobster, Crown of Thorns.

These species are **"bio-indicating"** species, which serve as indicators of the ecosystem health. These bio-indicating species are of course dependent on each region - here the focus is for Malaysia/Indo-Pacific region.

## 📊 Datasets Details

The models utilize a combination of publicly available datasets (~ 90%) and Tēnaka-based datasets (~ 10%). Some datasets were already annotated, and others undergo manual labeling.

References to the public datasets used can be found in the 'References' section of this README.

The images used with annotations (YOLO format) can be downloaded using the following links: [FishInv dataset](https://stpubtenakanclyw.blob.core.windows.net/marine-detect/FishInv-dataset.zip?sv=2022-11-02&ss=bf&srt=co&sp=rltf&se=2099-12-31T18:55:46Z&st=2025-02-03T10:55:46Z&spr=https,http&sig=w%2FTQzrECsYsjtkBXNnnuFtn%2BC06PkjgLxDgRw%2FaUUKI%3D), [MegaFauna dataset](https://stpubtenakanclyw.blob.core.windows.net/marine-detect/MegaFauna-dataset.zip?sv=2022-11-02&ss=bf&srt=co&sp=rltf&se=2099-12-31T18:55:46Z&st=2025-02-03T10:55:46Z&spr=https,http&sig=w%2FTQzrECsYsjtkBXNnnuFtn%2BC06PkjgLxDgRw%2FaUUKI%3D).

### Datasets split details

| Model          | Training + Validation Sets | Test Set     |
| -------------- | -------------------------- | --------     |
| FishInv        | 12,243 images (80%, 20%)   | 499  images  |
| MegaFauna      | 8,130 images (80%, 20%)    | 253  images  |

> [!NOTE]
> The rationale behind the development of two distinct models lies in the utilization of already annotated images available in public datasets. By having separate models, we sidestep the necessity of reannotating images that already encompass annotations for specific species with every Fish, Invertebrates and MegaFauna species.  For example, we found a lot of images of turtles already annotated. If we were to adopt a single, all-encompassing model for both Fish and Invertebrates Species 🐟 and MegaFauna 🦈, it would necessitate the reannotation of all those turtle images to include species like urchins, fishes, ...

## 🤖 Model Details

You can download the trained models using the following links: [FishInv model](https://stpubtenakanclyw.blob.core.windows.net/marine-detect/models/FishInv.pt?sv=2022-11-02&ss=bf&srt=co&sp=rltf&se=2099-12-31T18:55:46Z&st=2025-02-03T10:55:46Z&spr=https,http&sig=w%2FTQzrECsYsjtkBXNnnuFtn%2BC06PkjgLxDgRw%2FaUUKI%3D), [MegaFauna model](https://stpubtenakanclyw.blob.core.windows.net/marine-detect/models/MegaFauna.pt?sv=2022-11-02&ss=bf&srt=co&sp=rltf&se=2099-12-31T18:55:46Z&st=2025-02-03T10:55:46Z&spr=https,http&sig=w%2FTQzrECsYsjtkBXNnnuFtn%2BC06PkjgLxDgRw%2FaUUKI%3D).

<details>

<summary>MegaFauna model performances</summary>

| Class  | Images | Instances | mAP50 | mAP50-95 |
| ------ | ------ | --------- | ----- | -------- |
| ray    | 253    | 73        | 0.863 | 0.777    |
| shark  | 253    | 111       | 0.741 | 0.627    |
| turtle | 253    | 109       | 0.948 | 0.887    |

</details>

<details>

<summary>FishInv model performances</summary>

| Class                  | Images | Instances | mAP50 | mAP50-95 |
| ---------------------- | ------ | --------- | ----- | -------- |
| fish                   | 499    | 259       | 0.616 | 0.501    |
| serranidae             | 499    | 49        | 0.850 | 0.777    |
| urchin                 | 499    | 80        | 0.743 | 0.479    |
| scaridae               | 499    | 48        | 0.828 | 0.794    |
| chaetodontidae         | 499    | 65        | 0.891 | 0.827    |
| giant_clam             | 499    | 102       | 0.870 | 0.602    |
| lutjanidae             | 499    | 86        | 0.865 | 0.777    |
| muraenidae             | 499    | 58        | 0.949 | 0.809    |
| sea_cucumber           | 499    | 33        | 0.969 | 0.939    |
| haemulidae             | 499    | 22        | 0.972 | 0.945    |
| lobster                | 499    | 31        | 0.984 | 0.877    |
| crown_of_thorns        | 499    | 28        | 0.981 | 0.790    |
| bolbometopon_muricatum | 499    | 19        | 0.993 | 0.936    |
| cheilinus_undulatus    | 499    | 29        | 0.995 | 0.968    |
| cromileptes_altivelis  | 499    | 30        | 0.995 | 0.945    |

</details>

## 🚗 Usage

- flask app
- CLI interface
- live cam

### 🏁 Environment Setup

There are 3 options to install the development environment.



#### Developing on Your Host OS with PIP:

- Make sure pyenv is installed and working
- Then, run the following commands in the project directory:
```shell
git clone https://github.com/Way2skills/yolov8-deepsort.git

python -m venv env
env\Scripts\activate
pip install -r requirements.txt

#use any one 
python app.py #for flask app (image only)
python interface.py #for cli interface (image , video )
python live.py # for live camera
```
