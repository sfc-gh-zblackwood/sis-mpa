# SiS MPA Hack

Multipage streamlit apps aren't supported today (2022-01-13) in SiS, so I pulled
some code from [st_pages](https://github.com/blackary/st_pages), and it worked!

Example app: https://app.snowflake.com/sfcogsops/snowhouse_aws_us_west_2/#/streamlit-apps/TEMP.A_ST_SCHEMA.MPA_APP

1. Create an app with the code from streamlit_app.py
2. Update the page list at the bottom of the streamlit_app.py file
3. Upload all of the other pages to the stage of your app
4. Profit!