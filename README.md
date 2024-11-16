# Dicoding | Learn Data Analysis with Python | Data Analysis Project: Bike Sharing Dataset

[![wakatime](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/b0c149bc-9ee5-4f33-8d04-8de21aac863d.svg)](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/b0c149bc-9ee5-4f33-8d04-8de21aac863d)

## Project Description

This project explores the relationship between weather conditions and the total bike rentals. It also examines how bike rental trends differ between working days and weekends/holidays.

## Dataset Description

I am using the [Bike Sharing Dataset](https://github.com/ridwaanhall/dicoding-bike-sharing-analysis/tree/main/data) for this analysis.

## Installation Instructions

1. Clone the project repository:

    ```sh
    git clone https://github.com/ridwaanhall/dicoding-bike-sharing-analysis
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

    or you can use

    ```sh
    virtualenv venv
    ```

3. Activate the virtual environment and install the dependencies:

    ```sh
    # On Windows
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Usage Instructions

- To use this project, refer to the documentation in `notebook.ipynb`.
- To run the Streamlit dashboard, execute the following command:

```sh
streamlit run dashboard/dashboard.py
```

## Features

- Analysis of bike rentals across different seasons to determine the most and least popular seasons.
- Examination of the relationship between weather conditions and total bike rentals (`total`).
- Comparison of bike rental trends between working days (`workingday`) and weekends/holidays (`holiday`).
- RFM Analysis
- Display analysis results using Streamlit.

## Contributing

Contact me on LinkedIn/GitHub with the username `ridwaanhall` or send an email to `ridwaanhall.dev@gmail.com`. You can also submit a pull request.

## License

This project can be used for private usage. For commercial use, include my name and modify the code accordingly.
