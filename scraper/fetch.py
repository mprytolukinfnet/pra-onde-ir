from AirbnbScraper import AirbnbScraper

bot = AirbnbScraper()
df = bot.fetch()
df.to_csv('../data/airbnb_data.csv', index=False)