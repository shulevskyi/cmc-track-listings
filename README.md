## Instruction

That code provides access to pro-API from CoinMarketCap and grabs info about recently listed tokens.

### Dive into the structure

Let us find out about API. Pro-API provides faster data for the user than the Public API; thus, we can quickly grab data and apply it wherever needed.
It is more structured and ready for the developer. We use /map endpoint, and if we go to https://pro-api.coinmarketcap.com/v1/cryptocurrency/map, we will
find out that it grabs only one call for one request which is insane compared to /listing endpoint, which requires 25.
Therefore, with a limit of 10000 calls per month, we could maintain a server for 3.5 days; however, the limit is not such a big problem;
we will touch on this a bit later
  
##### Endpoint /cryptocurrency/map
This endpoint provides us with every cryptocurrency on CMC, even if it’s not listed yet. Applying the -1 index to the dataset gives us the last token
with listing status inactive, untracked or active. Currently, we building code on the untracked listing;

What does it mean? Simply, it means that when a token goes from inactive to untracked, it’s already on CMC; however, it has no access to everyone, so
it’s the perfect time to buy it. When it disappears from untracked, it goes to active, and it is a time when everyone may see it and most likely buy.
