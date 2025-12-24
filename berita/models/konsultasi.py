from odoo import api, fields, models

class KonsultasiData(models.Model):
    _name = "konsultasi.data"
    _description = "Konsultasi"

    name = fields.Char('Title')
    penanya = fields.Char('Nama Penanya')
    email = fields.Char("Email Penanya")
    alamat = fields.Char("Alamat Penanya")
    isi_pesan = fields.Char("Isi Pesan")
    tanggal = fields.Char("Tanggal")
    handphone = fields.Char("handphone")