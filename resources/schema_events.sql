CREATE TABLE IF NOT EXISTS tracking.events
(
	request_id CHAR(36) NOT NULL
	,request_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL
	,cookie_id CHAR(36) NOT NULL
	,topic VARCHAR(1024) NOT NULL
	,message VARCHAR(3128) 
	,environment VARCHAR(30) 
	,website_id CHAR(36) 
	,user_account_id CHAR(36) 
	,"location" VARCHAR(5000) 
	,user_agent VARCHAR(1024) 
	,referrer VARCHAR(500) 
)