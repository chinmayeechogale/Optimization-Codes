# Data

The dataset used in this project contains historical operating data from a coal-fired power plant (2022).

## Source

The dataset is publicly available on Kaggle:

**Dataset:** Power Plant Steam Turbine and Boiler Metrics (or similar — update this link once confirmed)

To download:
1. Create a free Kaggle account at [kaggle.com](https://www.kaggle.com)
2. Navigate to the dataset page
3. Download the CSV file
4. Place it in this `data/` folder
5. Rename it to `plant_data_2022.csv` (or update the filename in the surrogate model scripts)

## Variables in the Dataset

The raw dataset includes operating measurements for:
- Desuperheating water flows
- APH (air preheater) leakage
- Boiler energy input
- Feedwater temperature and flow
- Emission readings: SO₂, NOx, CO, CO₂, dust
- Performance indicators: NPHR, NTHR, HHV

## Preprocessing

Run the preprocessing script in `surrogate_models/` to:
- Clean and normalize the data
- Fit regression surrogate models for all outputs
- Save model coefficients for use in optimization scripts

> **Note:** The raw data file is not included in this repository to keep the repo lightweight. Please download it from Kaggle using the instructions above.
