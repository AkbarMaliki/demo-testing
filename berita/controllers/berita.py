import json
import os
import binascii
import logging
from odoo import _, fields, http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.web.controllers.home import Home as WebHome
from odoo.addons.web.controllers.utils import is_user_internal
from odoo.addons.portal.controllers.portal import CustomerPortal
from collections import defaultdict
import re
from datetime import datetime
_logger = logging.getLogger(__name__)

import json
from odoo.http import request, Response
from datetime import date
class BeritaController(http.Controller):
    @http.route("/news/feed", auth="public", methods=["GET"], csrf=False)
    def berita_news_feed(self, **params):
        module_path = os.path.dirname(os.path.realpath(__file__))
        src_path = os.path.join(module_path, "src")
        with open(
            os.path.join(src_path, "views", 'index.html'), "r", encoding="utf-8"
        ) as file:
            body = file.read()
        html_content = body
        return html_content

    @http.route("/konsultasi", auth="public", methods=["GET"], csrf=False)
    def konsultasi_web(self, **params):
        module_path = os.path.dirname(os.path.realpath(__file__))
        src_path = os.path.join(module_path, "src")
        with open(
            os.path.join(src_path, "views", 'konsultasi.html'), "r", encoding="utf-8"
        ) as file:
            body = file.read()
        html_content = body
        return html_content

    def _get_first_image_path(self, content):
        """Ambil path/URL src dari <img> pertama di HTML content."""
        if not content:
            return False
        match = re.search(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', content)
        if match:
            return match.group(1)
        return False

    @http.route("/api/v1/berita/populer", type="http", auth="public", methods=["GET"], csrf=False)
    def api_get_berita_populer(self, **kwargs):
        blogs = request.env['blog.post'].sudo().search(
            [],
            order="visits desc, post_date desc, create_date desc",
            limit=5
        )
        list_blog = []

        # Helper serialize datetime/date
        # Formatter tanggal ke "01 Desember 2025"
        def serialize_date(val):
            bulan_dict = {
                1: "Januari",
                2: "Februari",
                3: "Maret",
                4: "April",
                5: "Mei",
                6: "Juni",
                7: "Juli",
                8: "Agustus",
                9: "September",
                10: "Oktober",
                11: "November",
                12: "Desember",
            }
            if not val:
                return ""
            # val bisa type string ISO, datetime.datetime atau datetime.date
            dt = val
            if isinstance(val, str):
                try:
                    dt = datetime.fromisoformat(val)
                except Exception:
                    return val
            # Jika ada .date() method (datetime), ambil tanggalnya saja
            if hasattr(dt, "date"):
                dt = dt.date()
            try:
                hari = dt.day
                bulan = bulan_dict.get(dt.month, str(dt.month))
                tahun = dt.year
                return "{:02d} {} {}".format(hari, bulan, tahun)
            except Exception:
                return str(val)

        # Ambil url image company default jika diperlukan
        company = request.env.company
        company_image_url = False
        if getattr(company, "logo", False):
            company_image_url = '/web/image/res.company/{}/logo'.format(company.id)

        for blog in blogs:
            # Gambar default dari field image_1920
            image_url = False
            if hasattr(blog, 'image_1920') and getattr(blog, "image_1920", False):
                image_url = '/web/image/blog.post/{}/image_1920'.format(blog.id)

            # Ambil gambar pertama dari content (jika ada), fallback ke image company jika tidak ada
            first_content_image = self._get_first_image_path(blog.content or "")
            if not first_content_image:
                first_content_image = company_image_url

            list_blog.append({
                'is_published': blog.is_published,
                'author_name': blog.author_name,
                'content': blog.content,
                'name': blog.name,
                'subtitle': blog.subtitle,
                'published_date': serialize_date(blog.published_date),
                'post_date': serialize_date(blog.post_date),
                'website_url': blog.website_url,
                'image_url': image_url,                  # dari image_1920
                'content_image_url': first_content_image # dari <img> pertama di content atau fallback company image
            })

        response_data = {
            'data': list_blog,
        }

        return http.Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type="application/json;charset=utf-8",
            status=200,
        )


    @http.route("/api/v1/berita/terbaru", type="http", auth="public", methods=["GET"], csrf=False)
    def api_get_berita_terbaru(self, **kwargs):
        blogs = request.env['blog.post'].sudo().search(
            [],
            order="post_date desc, create_date desc",
            limit=5
        )
        list_blog = []

        # Helper serialize datetime/date
        # Formatter tanggal ke "01 Desember 2025"
        def serialize_date(val):
            bulan_dict = {
                1: "Januari",
                2: "Februari",
                3: "Maret",
                4: "April",
                5: "Mei",
                6: "Juni",
                7: "Juli",
                8: "Agustus",
                9: "September",
                10: "Oktober",
                11: "November",
                12: "Desember",
            }
            if not val:
                return ""
            # val bisa type string ISO, datetime.datetime atau datetime.date
            dt = val
            if isinstance(val, str):
                try:
                    dt = datetime.fromisoformat(val)
                except Exception:
                    return val
            # Jika ada .date() method (datetime), ambil tanggalnya saja
            if hasattr(dt, "date"):
                dt = dt.date()
            try:
                hari = dt.day
                bulan = bulan_dict.get(dt.month, str(dt.month))
                tahun = dt.year
                return "{:02d} {} {}".format(hari, bulan, tahun)
            except Exception:
                return str(val)

        # Ambil url image company default jika diperlukan
        company = request.env.company
        company_image_url = False
        if getattr(company, "logo", False):
            company_image_url = '/web/image/res.company/{}/logo'.format(company.id)

        for blog in blogs:
            # Gambar default dari field image_1920
            image_url = False
            if hasattr(blog, 'image_1920') and getattr(blog, "image_1920", False):
                image_url = '/web/image/blog.post/{}/image_1920'.format(blog.id)

            # Ambil gambar pertama dari content (jika ada), fallback ke image company jika tidak ada
            first_content_image = self._get_first_image_path(blog.content or "")
            if not first_content_image:
                first_content_image = company_image_url

            list_blog.append({
                'is_published': blog.is_published,
                'author_name': blog.author_name,
                'content': blog.content,
                'name': blog.name,
                'subtitle': blog.subtitle,
                'published_date': serialize_date(blog.published_date),
                'post_date': serialize_date(blog.post_date),
                'website_url': blog.website_url,
                'image_url': image_url,                  # dari image_1920
                'content_image_url': first_content_image # dari <img> pertama di content atau fallback company image
            })

        response_data = {
            'data': list_blog,
        }

        return http.Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type="application/json;charset=utf-8",
            status=200,
        )



    def _format_tanggal_indo(self, dt):
        """
        Format dt (date/datetime obj or string) jadi '01 januari 2025'
        """
        if not dt:
            return ""
        import datetime
        bulan_dict = {
            1: 'januari', 2: 'februari', 3: 'maret', 4: 'april',
            5: 'mei', 6: 'juni', 7: 'juli', 8: 'agustus',
            9: 'september', 10: 'oktober', 11: 'november', 12: 'desember'
        }
        if isinstance(dt, str):
            try:
                dt = datetime.datetime.strptime(dt, "%Y-%m-%d").date()
            except Exception:
                return dt
        elif isinstance(dt, datetime.datetime):
            dt = dt.date()
        try:
            hari = dt.day
            bulan = bulan_dict.get(dt.month, str(dt.month))
            tahun = dt.year
            return "{:02d} {} {}".format(hari, bulan, tahun)
        except Exception:
            return str(dt)

    @http.route('/berita/komentar', auth='public', methods=['GET'], csrf=False)
    def get_komentar(self, blog_id=None, **kw):
        """
        Get all komentar for a blog post by blog_id.
        """
        import json
        from odoo.http import request, Response

        if not blog_id:
            response_data = {'error': 'blog_id harus diisi'}
            return Response(
                json.dumps(response_data, ensure_ascii=False),
                content_type="application/json;charset=utf-8",
                status=200,
            )
        komentar_obj = request.env['blog.komentar'].sudo()
        komentar_records = komentar_obj.search([('blog_id', '=', int(blog_id))], order="id ASC")
        result = []
        for komentar in komentar_records:
            result.append({
                'id': komentar.id,
                'name': komentar.name,
                'pembuat': komentar.pembuat,
                'email': komentar.email,
                'comment': komentar.comment,
                'blog_id': komentar.blog_id.id,
                'tanggal_komentar': self._format_tanggal_indo(komentar.tanggal_komentar),
            })
        response_data = {'data': result}
        return Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type="application/json;charset=utf-8",
            status=200,
        )

    @http.route('/berita/komentar', auth='public', methods=['POST'], csrf=False)
    def post_komentar(self, **kwargs):
        """
        Create komentar for a blog post.
        Required: blog_id, pembuat, email, comment, (optional: name)
        """


        # Periksa apakah request Content-Type 'application/json' dan jika iya, baca dari body
        if request.httprequest.content_type == 'application/json':
            try:
                payload = json.loads(request.httprequest.data.decode('utf-8'))
            except Exception as e:
                response_data = {'error': f'JSON tidak valid: {str(e)}'}
                return Response(
                    json.dumps(response_data, ensure_ascii=False),
                    content_type="application/json;charset=utf-8",
                    status=200,
                )
            blog_id = payload.get('blog_id')
            pembuat = payload.get('pembuat')
            email = payload.get('email')
            comment = payload.get('comment')
            name = payload.get('name', "")
        else:
            # Fallback: data dari form-urlencoded / kwargs biasa
            blog_id = kwargs.get('blog_id')
            pembuat = kwargs.get('pembuat')
            email = kwargs.get('email')
            comment = kwargs.get('comment')
            name = kwargs.get('name', "")

        # Validasi field wajib
        if not (blog_id and pembuat and email and comment):
            response_data = {'error': 'blog_id, pembuat, email, dan comment harus diisi.'}
            return Response(
                json.dumps(response_data, ensure_ascii=False),
                content_type="application/json;charset=utf-8",
                status=200,
            )

        try:
            komentar_obj = request.env['blog.komentar'].sudo()
            tanggal_komentar = date.today()
            komentar_rec = komentar_obj.create({
                'name': name,
                'blog_id': int(blog_id),
                'pembuat': pembuat,
                'email': email,
                'comment': comment,
                'tanggal_komentar': tanggal_komentar,
            })
            response_data = {
                'success': True,
                'komentar_id': komentar_rec.id,
                'message': 'Komentar berhasil ditambahkan.',
                'tanggal_komentar': self._format_tanggal_indo(komentar_rec.tanggal_komentar),
            }
        except Exception as e:
            response_data = {'error': f'Terjadi kesalahan saat menambahkan komentar: {str(e)}'}
        
        return Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type="application/json;charset=utf-8",
            status=200,
        )

    @http.route('/berita/komentar/delete', auth='public', methods=['POST'], csrf=False)
    def delete_komentar(self, **kwargs):
        """
        Delete komentar based on komentar_id (required)
        """
        import json
        from odoo.http import request, Response

        # Bisa terima data dari JSON body atau form-urlencoded
        komentar_id = None
        if request.httprequest.content_type and 'application/json' in request.httprequest.content_type:
            try:
                payload = json.loads(request.httprequest.data.decode('utf-8'))
                komentar_id = payload.get('komentar_id')
            except Exception as e:
                response_data = {'error': f'JSON tidak valid: {str(e)}'}
                return Response(
                    json.dumps(response_data, ensure_ascii=False),
                    content_type="application/json;charset=utf-8",
                    status=200,
                )
        if not komentar_id:
            komentar_id = kwargs.get('komentar_id')

        if not komentar_id:
            response_data = {'error': 'komentar_id harus diisi.'}
            return Response(
                json.dumps(response_data, ensure_ascii=False),
                content_type="application/json;charset=utf-8",
                status=200,
            )
        try:
            komentar_obj = request.env['blog.komentar'].sudo()
            komentar_rec = komentar_obj.browse(int(komentar_id))
            if komentar_rec.exists():
                komentar_rec.unlink()
                response_data = {
                    'success': True,
                    'message': 'Komentar berhasil dihapus.',
                }
            else:
                response_data = {
                    'error': 'Komentar tidak ditemukan.'
                }
        except Exception as e:
            response_data = {'error': f'Terjadi kesalahan saat menghapus komentar: {str(e)}'}

        return Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type="application/json;charset=utf-8",
            status=200,
        )





    # API GET: Ambil semua data konsultasi
    @http.route('/api/v1/konsultasi', auth="public", methods=["GET"], csrf=False)
    def api_get_konsultasi(self, **params):
        records = request.env['konsultasi.data'].sudo().search([], order="id desc")
        result = []
        for rec in records:
            result.append({
                "id": rec.id,
                "title": rec.name,
                "penanya": rec.penanya,
                "email": rec.email,
                "alamat": rec.alamat,
                "isi_pesan": rec.isi_pesan,
                "tanggal": rec.tanggal,
                "handphone": rec.handphone,
            })
        response_data = {
            "data": result,
            "count": len(result)
        }
        return Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type="application/json;charset=utf-8",
            status=200,
        )

    # API POST: Buat entri konsultasi baru
    @http.route('/api/v1/konsultasi',  auth="public", methods=["POST"], csrf=False)
    def api_post_konsultasi(self, **params):
        required_fields = ["penanya", "isi_pesan"]
        data = params if params else {}
        if not data and request.httprequest.data:
            try:
                data = json.loads(request.httprequest.data.decode("utf-8"))
            except Exception:
                data = {}
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            response_data = {
                "error": "Field berikut harus diisi: %s" % ", ".join(missing)
            }
            return Response(
                json.dumps(response_data, ensure_ascii=False),
                content_type="application/json;charset=utf-8",
                status=200,
            )

        new_rec = request.env['konsultasi.data'].sudo().create({
            "name": data.get("title") or "",
            "penanya": data.get("penanya"),
            "email": data.get("email") or "",
            "alamat": data.get("alamat") or "",
            "isi_pesan": data.get("isi_pesan"),
            "tanggal": data.get("tanggal") or "",
            "handphone": data.get("handphone") or "",
        })
        response_data = {
            "success": True,
            "id": new_rec.id,
            "message": "Konsultasi berhasil dikirim.",
        }
        return Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type="application/json;charset=utf-8",
            status=200,
        )
