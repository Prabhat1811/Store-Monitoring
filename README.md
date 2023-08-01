### Tools used

1. FastAPI - Python
2. SQLite

### Running the project

1. Install conda
2. Run the following commands in your terminal
   1. `conda create -n loop`
   2. `conda activate loop`
   3. `pip install -r requirements.txt`
   4. `uvicorn app.main:app --reload`

## Observations

1. Time to load >=2 million records (After processing) from csv to db ≈ 5 minutes
2. Time to generate csv from the data (Including processing) ≈ 6 minutes
3. These times are way too much and can be brought down to less than half of what they are

## Logic

### Determining active/inactive between logs

There is a problem and that is the gaps in the logs. `e.g. store_id=6921452823375303736`

We receive logs in one hour time intervals more or less. There can be 4 transitions from the previous state, Here's how we determine the time up/down between them.

<b>Note - We talk about the state that the store was in between any two status logs.</b>

1. `active -> inactive` - Store was active. Went down when we received inactive.
2. `active -> active` - Store was active.
3. `inactive -> active` - Store was inactive. Came up when we received active.
4. `inactive -> inactive` - Store was inactive.

We also don't know status of the store when the state comes/goes to unknown i.e. before/after the first/last log. We will calculate it on the basis of the first/last state.

1. `unknown -> active` - Was active.
2. `unknown -> inactive` - Was inactive.
3. `active -> unknown` - Was active.
4. `inactive -> unknown` - Was inactive.

## Questions

```
<Ques.> How would you access files created in the past?
<Ans.> Right now, You can't.
```

```
<Ques.> What would happen when multiple users call `/trigger_report` endpoint?
<Ans.> Right now. The system will put a lock when a user calls the `/trigger_report` endpoint and the lock will be intact until the report is finished hence preventing race condition.

To make it more scalable, We can set up asynchronous tasks. It would also be good for our API server as It won't be busy creating reports and would focus on user requests.

This will also solve when two requests come in simultaneously.
```
