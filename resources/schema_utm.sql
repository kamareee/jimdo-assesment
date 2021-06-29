CREATE TABLE IF NOT EXISTS tracking.utm
(
	request_id VARCHAR(56) NOT NULL  ENCODE zstd
	,source VARCHAR(255) NOT NULL  ENCODE zstd
	,medium VARCHAR(255) NOT NULL  ENCODE zstd
	,campaign VARCHAR(255)   ENCODE zstd
	,content VARCHAR(255)   ENCODE zstd
	,term VARCHAR(255)   ENCODE zstd
	,matchtype VARCHAR(255)   ENCODE zstd
	,"network" VARCHAR(255)   ENCODE zstd
	,ad_id VARCHAR(255)   ENCODE zstd
	,ad_pos VARCHAR(255)   ENCODE zstd
	,placement VARCHAR(255)   ENCODE zstd
	,placement_category VARCHAR(255)   ENCODE zstd
	,testgroup VARCHAR(255)   ENCODE zstd
	,device VARCHAR(255)   ENCODE zstd
)