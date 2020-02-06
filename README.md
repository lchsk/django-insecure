# Simple Django application with a number of built-in security vulnerabilities

Corresponding article with examples and explanation: [Stay paranoid and trust no one. Overview of common security vulnerabilities in web applications](https://lchsk.com/stay-paranoid-and-trust-no-one-overview-of-common-security-vulnerabilities-in-web-applications.html)

Some of them are detected with [bandit](https://github.com/PyCQA/bandit)

Run it like this:

```
bandit -r ./insecure/security
```

To start the server:

```
python manage.py runserver
```

Contains examples of threats:

- SQL injection

- Command injection

- Insecure deserialization (unsafe use of Python `pickle`)

- Cross-site scripting (XSS)
