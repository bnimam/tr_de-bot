FROM python:3.9-slim

RUN pip3 install discord yfinance wallstreet

COPY /tr_de-bot/* /tr_de-bot/

CMD ["python3 /tr_de-bot/trade-bot.py"]