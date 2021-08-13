import requests


def get_prices():
    coins = ["BTC", "ETH", "DOGE"]

    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=INR".format(",".join(coins))).json()["RAW"]

    data = {}
    for i in crypto_data:
        data[i] = {
            "coin": i,
            "price": crypto_data[i]["INR"]["PRICE"],
            "change_day": crypto_data[i]["INR"]["CHANGEPCT24HOUR"],
            "change_hour": crypto_data[i]["INR"]["CHANGEPCTHOUR"]
        }

    return data


if __name__ == "__main__":
    print(get_prices())