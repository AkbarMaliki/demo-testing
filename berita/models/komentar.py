from odoo import api, fields, models

class KomentarBlog(models.Model):
    _name = "blog.komentar"
    _description = "Blog Komentar"

    name = fields.Char('Title')
    blog_id = fields.Many2one('blog.post')
    pembuat = fields.Char("Pembuat Komentar")
    email = fields.Char("Email Komentar")
    comment = fields.Char("Komentar")
    tanggal_komentar = fields.Date('Tanggal Komentar')