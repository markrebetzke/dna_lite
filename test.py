import requests, json

def get_employee_Data():
    #url = "http://dummy.restapiexample.com/api/v1/employees"
    url = "https://reqres.in/api/users"
    payload = {}
    headers = {'Accept':'applcation/json'}
    response = requests.get(url=url, headers=headers, data=payload)
    resp = response.json()
    print(resp['data'][0]['id'])
    print(resp['data'][0]['email'])

    for x, y in resp.items():
        if x == 'data':
            print(x[0])
    return resp

def main():
    get_employee_Data()

main()