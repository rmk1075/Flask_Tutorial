# Templates

## 2021.02.21

<details>

<summary>Jinja Setup</summary>

- Flask에서 Jinja2의 기본설정

  - render_template() 사용시, .html, .xml 등의 템플릿 파일들에 대해서 autoescaping(자동변환) 활성화
  
  - render_template_string() 사용시, 모든 문자열에 대해서 autoescaping 활성화

  - {% autoescaping %} 태그 사용해서 자동변환 사용

  - Flask는 기본적으로 Jinja2 컨텍스트(context)를 통해서 전역 함수들과 헬퍼함수들을 제공한다

</details>

<details>

<summary>Standard Context</summary>

- Jinja2 template에서 사용할 수 있는 글로벌 변수

- config

  - The current configuration object (flask.config)

- request

  - The current request object (flask.request).
  
  - This variable is unavailable if the template was rendered without an active request context.

- session

  - The current session object (flask.session).
  
  - This variable is unavailable if the template was rendered without an active request context.

- g

  - The request-bound object for global variables (flask.g).
  
  - This variable is unavailable if the template was rendered without an active request context.

- url_for()

- get_flashed_messages()

</details>

<details>

<summary>Standard Filters</summary>

- tojson()

  - 주어진 객체를 json 형식으로 변환한다.

```html
<script type=text/javascript>
    doSomethingWith({{ user.username|tojson }});
</script>

<button onclick='doSomethingWith({{ user.username|tojson }})'>
    Click me
</button>
```

</details>

<details>

<summary>Controlling Autoescaping</summary>

- autoescaping: 자동으로 특수문자들을 변환시켜주는 개념

  - 특수문자 &, >, <, ", '

  - 해당 문자들은 기본적으로 문서내에서 특수한 의미를 가지고 사용되는 문자들이기 때문에 해당 의미없이 텍스트로 사용하기 위해서는 entities로 변환해야한다.

- autoescaping 제어 방법

  1) python 코드에서 HTML 문자열을 템플릿에 전달되기 전에 markup 객체로 감싸준다.

  2) Template 내부에서 |safe 필터를 통해서 문자열을 안전한 html이 되도록 한다. ex) {{ myvariable|safe }}

  3) 일시적으로 autoescaping을 중단한다. - {% autoescape %} 블럭을 사용

```html
{% autoescape false %}
    <p>autoescaping is disabled here
    <p>{{ will_not_be_escaped }}
{% endautoescape %}
```

</details>

<details>

<summary>Registering Filters</summaruy>

- Jinja2 템플릿에서 filter 등록해서 사용하는 방법

  1) jinja_env에 등록해서 사용

  2) template_filter() 데코레이터 사용

```python
# 1번 방법
def reverse_filter(s):
    return s[::-1]
app.jinja_env.filters['reverse'] = reverse_filter

# 2번 방법
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]
```

- 템플릿에서 사용예제

```jinja
{% for x in mylist | reverse %}
{% endfor %}
```

</details>

<details>

<summary>Context Processors</summary>

- context processor: 새로운 변수들을 template context에 주입시키기 위해서 사용

  - 새로운 변수들을 template context에 주입하기 위해서 렌더링 전에 실행된다.

  - dict 객체를 반환한다.

  - 이 dict 객체의 키와 밸류는 전체 template context에 통합된다.

```python
# user라는 변수를 템플릿 내부에서 g.user의 값으로 사용할 수 있도록 설정
@app.context_processor
def inject_user():
    return dict(user=g.user)

# format_price() 함수를 템플릿에서 사용할 수 있도록 설정
@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)
    return dict(format_price=format_price)
```

```jinja
<!-- 템플릿에서 해당 함수 사용 예제 -->
{{ format_price(0.33) }}
```

</details>
