# Aikabu

A Python 3 library for interacting with the [AiKaBu](http://aikabu.jp/) private API.

### Obtaining your account_token
I found one mine by using [Fiddler](http://www.telerik.com/fiddler).  
[mitmproxy](https://mitmproxy.org/) is also useful for this.

### Dependencies

[Requests](http://docs.python-requests.org/en/latest/)  

    pip install -r requirements.txt

### Example API usage

```python  
from aikabu import Aikabu

account_token = "abc123"  
akb = Aikabu(account_token)  
print(akb.stock_summaries())  

```
