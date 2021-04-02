# Project Title
The correspondence of max-flow to the absolute permeability of porous systems 


## Motivation

This code is developed to undertake computations and visualisations included in the submitted manuscript. The main idea is to make the results of this research easily reproducible.

## Getting Started
```
git clone https://github.com/AleksZhuravlyov/mincut_maxflow_pnm
cd mincut_maxflow_pnm

python3 -m pip install -r requirements.txt

python3 processing/artificial_processing.py
python3 processing/real_processing.py

python3 visualization/plot_k_pnm_edm.py
python3 visualization/plot_max_radius_min_cut_hist.py
python3 visualization/plot_min_cut_max_flow_demo.py
python3 visualization/plot_pairs.py
```
### Prerequisites

The libraries you need to install and how to install them

#### macOS:
```
brew install python@3.9
```
#### Ubuntu:
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9
```

## Brief description
The developed code has the following key features:

- Generation of artificial porous images;
- Extraction of pore networks (PN) from segmented digital images (real and artificial);
- Simulation of one-phase fluid flow through extracted PN;
- Computation of min-cut and maximum-flow in a network by the Edmonds-Karp algorithm;
- Establishment of the correspondence between min-cut max-flow and hydrodinamic permeability values of a network;
- Calcualtion of the critical radius from the digital image;
- Correlation analysis between various PN parameters.


## Publications

Armstrong, R.T., Lantec, Z., Mostaghimi, P., Zhuravljov, A., Herring, A., Robins, V. (2021). Correspondence of max-flow to the absolute permeability of porous systems. Physical Review Fluids (editorially approved for publication).


## Authors

This code was developed by
- [**Aleksandr Zhuravlyov**](https://github.com/AleksZhuravlyov/)
- [**Zakhar Lanets**](https://github.com/lanetszb/)

under the supervision of

- [**A/Prof Ryan T. Armstrong**](https://www.unsw.edu.au/engineering/our-people/ryan-armstrong)


## License

This project is licensed under the MIT License which is a permissive free software license originating at the Massachusetts Institute of Technology (MIT) - see the [LICENSE](LICENSE) file for details

