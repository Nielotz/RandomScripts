PYTHON_VERSION="3.11.2"
PYTHON_BRANCH="3.11"
PYTHON_COMPILED_OUTPUT="/home/pc/python$PYTHON_VERSION"
PYTHON_TEMP_FOLDER="_python$PYTHON_VERSION"

echo "Updating system"
sudo parrot-upgrade

echo "Downloading python into:" $PYTHON_TEMP_FOLDER
rmdir $PYTHON_TEMP_FOLDER  # Clean
mkdir $PYTHON_TEMP_FOLDER
cd $PYTHON_TEMP_FOLDER

git clone --single-branch --branch $PYTHON_BRANCH https://github.com/python/cpython.git 


echo "Instaling dependencies"
sudo apt-get update
sudo apt-get -y install build-essential python3-dev python3-setuptools python3-pip python3-smbus &&
	libncursesw5-dev libgdbm-dev libc6-dev &&
	zlib1g-dev libsqlite3-dev tk-dev &&
	libssl-dev openssl &&
	libffi-dev


echo "Configuring"
cd cpython
./configure --enable-optimizations --prefix=$PYTHON_COMPILED_OUTPUT --exec-prefix=$PYTHON_COMPILED_OUTPUT --with-openssl=/usr


echo "Make'ing"
make -j 12 # alternatively `make -j 4` will utilize 4 threads


echo "Installing"
sudo make altinstall


echo "Test:"
$PYTHON_COMPILED_OUTPUT/bin/python$PYTHON_BRANCH --version


echo "Cleaning..."
rm $PYTHON_TEMP_FOLDER -r