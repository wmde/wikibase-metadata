# Data Schedule

Data pulls occur on a rolling, scheduled basis. Once weekly, the server checks the database for observations that are stale or imminently so, and attempts to pull fresh data.

A Wikibase's observation is considered stale under the following conditions:

| Observation Type    | Last Observation Successful | Last Observation Unsuccessful |
| ------------------- | --------------------------- | ----------------------------- |
| Connectivity        | >=4 weeks                   | >=1 week                      |
| First Month Log     | >=52 weeks                  | >=40 weeks                    |
| Last Month Log      | >=4 weeks                   | >=1 week                      |
| Property Popularity | >=4 weeks                   | >=1 week                      |
| Quantity            | >=4 weeks                   | >=1 week                      |
| Software Version    | >=4 weeks                   | >=1 week                      |
| Statistics          | >=4 weeks                   | >=1 week                      |
| User Data           | >=4 weeks                   | >=1 week                      |

That is, for Connectivity Observations, if a Wikibase's most recent observation was successful, it is considered stale if that observation is more than 4 weeks old. If the most recent observation was _unsuccessful_, it is considered stale if that observation is more than 1 week old.
