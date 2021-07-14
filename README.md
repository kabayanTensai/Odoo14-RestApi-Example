# README
Basically this Repo just to prove that its easy to create REST-API on ODOO 14  and integrate it with other service like API-GATEWAY, on this demo It's focusing on Sale Order Activity 

## How To run On Localdevlopment

To Run This Example Of Rest API in  Odoo just run docker-compose up, Before run docker-compopse make sure create the volume
` docker volume create --name=db-data-14 ` and ` docker volume create --name=web-data-14`

* To configure webhook url in odoo go to sale -> settings -> scroll to the bottom of the page there will be 2 field that you need to set, Api Key field and Base URL for webhook interceptor ![enter image description here](https://i.imgur.com/yooOc9R.png) , basically if you run both app from docker-compose all you have to do just set url point to http://interceptor:<port>, 
* You can get Api key after register your account with interceptor service on this endpoint `http://localhost:5000/api/auth/signup` with json body `{"email":<your_email>}`

* Odoo Api_rest swagger https://localhost:8069/api_rest/swagger_doc

## To Run Interceptor Service only
to run Interceptor Service need to install python 3.9 on your system then
* run `pip install -r requirement.txt`
* setup config.py according to your need
* flask run
## List of Endpoint on Interceptor Service 
* `[GET]: /api/saleorder/list`
	* This Endpoint for list every available sale.order on Odoo
	* With Token  got from `/api/auth/login` set Header with `Authorization Bearer <your_token>`
* `[GET]: /api/saleorder/<id>`
	* 	This Endpoint for get sale.order by Id 
	* With Token  got from `/api/auth/login` set Header with `Authorization Bearer <your_token>`
* `[POST]: /api/webhook/saleorder`
	* This Endpoint to create Sale order
	* With Token  got from `/api/auth/login` set Header with `Authorization Bearer <your_token>
	* Json Body Example 

	        {
	      "name": "ASD-852/FDR/01/126",
	      "partner_id": 11,
	      "date_order": "2021-06-10 06:47:27",
	      "company_id": 1,
	      "order_line": [
	        {
	          "product_id": "31",
	          "product_uom_qty": 1,
	          "product_uom": 24,
	          "price_unit": 40000
	        }
	      ] }
* `[PUT]: /api/webhook/saleorder`
	* This Endpoint to Update Sale order
	* With Token  got from `/api/auth/login` set Header with `Authorization Bearer <your_token>
	* Json Body Example 

	        {
	      "name": "ASD-852/FDR/01/126",
	      "partner_id": 11,
	      "date_order": "2021-06-10 06:47:27",
	      "company_id": 1,
	      "order_line": [
	        {
	          "product_id": "31",
	          "product_uom_qty": 1,
	          "product_uom": 24,
	          "price_unit": 40000
	        }
	      ] }
* `/api/auth/signup`
	* This endpoint for registering new user for accessing Interceptor Service
	* Json Body Example	`{"email":"habibi@gmail.com"}`
	* response from this endpoint will be your apikey for auth `{"id": "bb2f5600c5a08bc1e85797478f56c7ad"}`

* `/api/auth/login`
	* This Endpoint for authenticating and get the JWT token
	* Json Body Example `{"apikey":"bb2f5600c5a08bc1e85797478f56c7ad"}`

## Webhook
Everytime there's CRUD process happened on Sale order, Odoo will send notification with payload(what's changes) to interceptor service with this format

    {
    "event":<model_domain>.<event>
    "payload":{<field>:<value>}
    }

