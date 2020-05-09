# plotly-test
This is my plotly learning repository. At first I just wanted to plot choropleth maps with covid19 data, but it turned out to be a nice intro to dash and heroku as well. Several things still need to be improved, but I hope this repo can help anyone who wants to learn about plotly-dash.

To run the `app.py` you need to install dash in your environtment and create the [mapbox token](https://account.mapbox.com/access-tokens/), then put the `.mapbox_token` file in the same directory. To run the file, simply type `pyhton app.py` in your terminal.

For those who want to push the `app.py` file to heroku, you need to create the `Procfile` and `requirements.txt` files. I mostly follow the guide on [plotly page](https://dash.plotly.com/deployment) except for the `requirements.txt` file. I aslo found the [Heroku Getting Started page](https://devcenter.heroku.com/articles/getting-started-with-python) is useful.

Lastly, check out these two amazing documentations on plotly-dash:
1. [New York recycling center.](https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Dash_Interactive_Graphs/Scatter_mapbox/recycling.py)
2. [SONYC-Dash-App.](https://github.com/amyoshino/SONYC-Dash-App/blob/master/app.py#L337)

Cheers.
