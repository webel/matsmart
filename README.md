# Check Matsmart for interesting items

## Description
In Sweden we have the brilliant online store [matsmart](www.matsmart.se) that sells products nearing their sell-by-date. 

A problem my partner and I have is the unnecessary amount of "window"-shopping, and the time it takes, when browsing Matsmart.

So, I built this rudimentary script to check the Matsmart API for "interesting items", e.g. items that are specified in a list in the `matsmart.py` module. The script will create `available_items.json` in the directory, which one can in turn open and format in ones favourite editor! 

## Installing and running the script
### Prepare
```sh
> python3 -m venv env
> . ./env/bin/active
> pip install -r requirements.txt
```

### Run
Change the `interesting_item_list` in `matsmart.py` with whatever you deem interesting, or just run as is to see what I find interesting (buckwheat, quinoa, chia...).

```sh
python -m matsmart
```

### Test
Absolutely most simple test has been included, for my purposes mostly when refactoring, to check that the mechanisms extracting `available_items` indeed do what they're supposed to. That's why there is a `test_data` folder.

```sh
python -m test
```

Prints "Passed" to console if the expected data is returned from `matsmart.py`.

## Further development
I primarily poke about in this repo while watching telly or listening to podcasts – it isn't the most serious endevour – but I do hope to accomplish these things in a timely manner;

[ ] Load "interesting items" from a csv document dumped in the directory (*this corresponds to how my partner and I go about bulk purchasing food and keeping our grocery costs low*)

[ ] Compare the kg price with the csv dumped in the directory (*we keep note of the cheapest bulk prices we find online in our `food.csv`*)

[ ] Check if json files are older than a day, then get fresh data from API (I don't want to poll the API every time I run the script, I don't know what Matsmart even thinks about using their API)

[ ] Build a simple front-end with links directly to the Matsmart product 

Many more thoughts regarding this project, like; 
- checking other online grocery sites for deals,
- making tests more independant (I don't want to be "aware" of tests in my non-test modules), 
- possibly adding a database such that the front-end can be interacted with and saving that data (ex. I don't want to see this product again, only show this if price drops below, etc).