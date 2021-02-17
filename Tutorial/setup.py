from setuptools import find_packages, setup
'''
- packages: include할 패키지 디렉토리
- find_packages(): 자동으로 python package들을 찾아준다.
- include_package_data: static file들이나 templates 디렉토리를 사용하기 위해서 True로 설정
   -> package data들에 대해서 설명하는 MANIFEST.in 파일이 필요
'''
setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)