## Instalação do Open CV nas Raspberry Pi B
- Executar o script **OpenCV_Raspbian.sh** em modo super-usuário. 
	- Esse script irá atualizar o python da raspberry, de modo manual, para uma versão mais moderna da linguagem (3.6.0)
- Após esse procedimento seguir os passos do link abaixo:
	- https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

- Algumas ressalvas devem ser consideradas:
	- Quando criado o ambiente virtual para a instalação do OpenCV, deve se observar qual a versão do python instalada no VirtualEnv criado. Está irá modificar o caminho dos arquivos. Possivelmente será instalado a versão 3.5.1 do python. Assim deve-se utilizar o caminho: 
```
/usr/local/lib/python3.5/site-packages/
```
- Em vez de

```
/usr/local/lib/python3.4/site-packages/
```
- Quando a função cmake for utilizada deve-se utilizar o comando abaixo **e não o comando indicado pelo link**:
```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    -D BUILD_EXAMPLES=ON ..
```

- Quando for realizar a edição do ` ~/.profile`, deve se utilizar os seguintes comandos listados abaixo: **(Não editar o arquivo diretamente!!!)**
```
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

```
