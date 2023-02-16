# Real estate web scraper
With the help of this tool, users can take useful information from real estate websites and put it in an AWS DynamoDB database for simple management and analysis. Users can extract details about properties, including their costs, locations, features, and other crucial information, using this online scraper. The project was created in Python and interacts with AWS using a number of tools, including ApiGateway, Lambda and others.

*This undertaking also serves as a data source for my [thesis](https://git.kpi.fei.tuke.sk/kpi-zp/2024/dp.adrian.pavlik/thesis). The collected data will be analyzed to identify trends and patterns in the real estate market.*


<br/>

## Supported websites
Please note that the app is only supported only for Slovak market, since I study there, and there are no future plans to add non-domestic websites support ***yet***.

<div align="center">

| Website | Fully supported | Partialy supported |
| ----------- |:-----------:|:-----------:|
| [reality.sk](https://www.reality.sk) | ⬜ | ⬜
| [nehnutelnosti.sk](https://www.nehnutelnosti.sk) |⬜ | ⬜
| [topreality.sk](https://www.topreality.sk/) |⬜ | ⬜
| [bazos.sk](https://reality.bazos.sk/inzeraty/) |⬜ | ⬜
| [zoznamrealit.sk](https://www.zoznamrealit.sk/) |⬜ | ⬜

</div>

<br/>

## Enviroment variables
You can download enviroment variables, needed for the code to work [here](https://drive.google.com/file/d/17PlPcqhIzxom6ggdlRVTqGVyGuLXC34u/view?usp=sharing).

<br/>

## Installing libraries
`pip install -r .\packages.txt`