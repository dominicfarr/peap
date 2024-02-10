echo "alias xpmain='poetry run python src/main.py --config config.json'" >> /root/.bashrc
echo "alias xpapp='poetry run python src/app.py'" >> /root/.bashrc
echo "alias xprx='poetry run python '" >> /root/.bashrc
echo "alias xpt='poetry run pytest .'" >> /root/.bashrc
echo "alias xrf='poetry run ruff format .'" >> /root/.bashrc
echo "alias ll='ls -las'" >> /root/.bashrc

# Set Git user name
git config --global user.name "Dommo"

# Set Git user email
git config --global user.email "dominic@formulathoughts.com"