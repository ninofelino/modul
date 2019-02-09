sudo mount.cifs //192.168.1.254/posserver /mnt/poserver share -o user=nuansa,password=nuansa,vers=2.1
sudo systemctl stop odoo
odoo -c odoo.conf