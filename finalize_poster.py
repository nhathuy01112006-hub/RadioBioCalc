#!/usr/bin/env python3
"""Build an A2 academic project poster and (after deployment) functional QR codes.
Run with --site-url https://USERNAME.github.io/REPOSITORY/ after verifying a live URL.
Optional --poster-url permits a separately hosted poster.
When called without URLs, deliberately renders labelled QR placeholders rather than invalid URLs.
"""
import argparse, math, textwrap
from pathlib import Path
from urllib.parse import urljoin, urlparse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A2
import qrcode
from PIL import Image
import fitz

BASE=Path(__file__).resolve().parents[1]
P=BASE/'poster';P.mkdir(parents=True,exist_ok=True)
fonts='/usr/share/fonts/truetype/dejavu'
pdfmetrics.registerFont(TTFont('DejaVu',fonts+'/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold',fonts+'/DejaVuSans-Bold.ttf'))
W,H=A2
NAVY=HexColor('#0A2444'); DEEP=HexColor('#0B345A');BLUE=HexColor('#087CB7'); TEAL=HexColor('#0C9C9D');PAPER=HexColor('#F3F7FB');GRAY=HexColor('#526477');INDIGO=HexColor('#5145CB');ORANGE=HexColor('#DC7607');GREEN=HexColor('#12856B');BORDER=HexColor('#DCE6F1')

def top_rect(c,x,top,w,h,fill,stroke=None,r=0):
 c.setFillColor(fill);c.setStrokeColor(stroke or fill)
 (c.roundRect if r else c.rect)(x,H-top-h,w,h,r,fill=1,stroke=int(stroke is not None)) if r else c.rect(x,H-top-h,w,h,fill=1,stroke=int(stroke is not None))

def line(c,x1,t1,x2,t2,color=BORDER,linewidth=1):
 c.setStrokeColor(color);c.setLineWidth(linewidth);c.line(x1,H-t1,x2,H-t2)

def txt(c,x,top,text,size=12,color=NAVY,bold=False):
 c.setFillColor(color);c.setFont('DejaVuBold' if bold else 'DejaVu',size);c.drawString(x,H-top-size,text)

def center_txt(c,x,top,text,size=12,color=NAVY,bold=False):
 c.setFillColor(color);c.setFont('DejaVuBold' if bold else 'DejaVu',size);c.drawCentredString(x,H-top-size,text)

def multiline(c,x,top,text,width,size=12,color=GRAY,leading=None,bold=False,max_lines=None):
 font='DejaVuBold' if bold else 'DejaVu';leading=leading or size*1.5
 lines=simpleSplit(text,font,size,width)
 if max_lines: lines=lines[:max_lines]
 for i,s in enumerate(lines):txt(c,x,top+i*leading,s,size,color,bold)
 return top+len(lines)*leading

def fit_img(c,path,x,top,w,h,mode='contain'):
 im=Image.open(path).convert('RGB')
 iw,ih=im.size
 if mode=='cover':
  crop_target=w/h
  if iw/ih>crop_target:
   nw=int(ih*crop_target); ox=(iw-nw)//2; im=im.crop((ox,0,ox+nw,ih))
  else:
   nh=int(iw/crop_target); oy=(ih-nh)//2; im=im.crop((0,oy,iw,oy+nh))
  c.drawImage(ImageReader(im),x,H-top-h,width=w,height=h,mask='auto')
 else:
  s=min(w/iw,h/ih);dx=(w-iw*s)/2;dy=(h-ih*s)/2
  c.drawImage(ImageReader(im),x+dx,H-top-h+dy,width=iw*s,height=ih*s,mask='auto')

def qr_image(url,path):
 qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=14,border=4)
 qr.add_data(url);qr.make(fit=True)
 qr.make_image(fill_color='#092B4D',back_color='white').convert('RGB').save(path)

def draw_qr_or_placeholder(c,path,x,top,size,label):
 top_rect(c,x,top,size,size,HexColor('#FFFFFF'),BORDER,10)
 if path and path.exists(): fit_img(c,path,x+8,top+8,size-16,size-16)
 else:
  c.setStrokeColor(HexColor('#CDD7E4')); c.setDash(5,4)
  c.roundRect(x+12,H-top-size+12,size-24,size-24,6,fill=0,stroke=1)
  c.setDash()
  center_txt(c,x+size/2,top+42,'QR',26,GRAY,True)
  center_txt(c,x+size/2,top+78,'CHƯA CÓ LINK',9,GRAY,True)

def make_pdf(site_url=None,poster_url=None):
 qrweb=P/'QR_Website.png';qrposter=P/'QR_Poster.png'
 if site_url:
  if not site_url.endswith('/'):site_url+='/';
  poster_url=poster_url or urljoin(site_url,'poster/RadioBioCalc_Poster.pdf')
  qr_image(site_url,qrweb); qr_image(poster_url,qrposter)
 else:
  for f in (qrweb,qrposter):
   if f.exists():f.unlink()
 out=P/'RadioBioCalc_Poster.pdf'; c=canvas.Canvas(str(out),pagesize=A2,pageCompression=1)
 c.setTitle('RadioBioCalc | Poster seminar Hypofractionation | Nhóm 4')
 top_rect(c,0,0,W,H,PAPER)
 # Header
 top_rect(c,0,0,W,230,NAVY)
 top_rect(c,0,220,W,11,BLUE)
 # subtle circles/lines decoration
 c.setStrokeColor(Color(.3,.65,.85,.14));c.setLineWidth(2)
 for r in [120,190,280]:c.circle(W-82,H-25,r,fill=0,stroke=1)
 # logos cards
 top_rect(c,40,36,115,118,HexColor('#FFFFFF'),None,15)
 fit_img(c,BASE/'assets/logo_truong.jpg',49,46,97,98)
 top_rect(c,W-155,36,115,118,HexColor('#FFFFFF'),None,15)
 fit_img(c,BASE/'assets/logo_khoa.jpg',W-146,46,97,98)
 center_txt(c,W/2,31,'ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH',13,HexColor('#A8D8FA'),True)
 center_txt(c,W/2,56,'TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN',20,HexColor('#FFFFFF'),True)
 center_txt(c,W/2,86,'KHOA VẬT LÝ – VẬT LÝ KỸ THUẬT',15,HexColor('#D2ECFC'),True)
 center_txt(c,W/2,118,'RadioBioCalc',48,HexColor('#FFFFFF'),True)
 center_txt(c,W/2,183,'HỆ THỐNG MÔ PHỎNG BED & PHÂN LIỀU XẠ TRỊ',17,HexColor('#D5E7F5'),True)
 center_txt(c,W/2,207,'SEMINAR SINH HỌC BỨC XẠ  •  HYPOFRACTIONATION  •  NHÓM 4',10.5,HexColor('#97C9ED'),True)
 # Home panel
 txt(c,40,253,'01  TỔNG QUAN WEBSITE',17,NAVY,True)
 line(c,40,284,W-40,284)
 top_rect(c,40,300,735,288,HexColor('#FFFFFF'),BORDER,16)
 home=BASE/'assets/previews/home.png'
 if home.exists():
  im=Image.open(home).convert('RGB')
  # website header + main banner only: screenshot top 0..530
  im=im.crop((65,0,min(1375,im.width),min(565,im.height)))
  fit_img(c, _tmp_pic(im, P/'_poster_home_tmp.jpg'),52,312,710,254,'contain')
 txt(c,790,315,'TRANG CHỦ',13,BLUE,True)
 multiline(c,790,345,'Hai logo nhận diện, thông tin nhóm, giới thiệu mục tiêu và lối truy cập 4 công cụ tính toán.',W-835,13,GRAY,20)
 top_rect(c,790,460,W-830,104,HexColor('#E6F4FD'),None,12)
 txt(c,807,473,'THIẾT KẾ ĐẶC TRƯNG',11,BLUE,True)
 multiline(c,807,498,'Xanh y khoa • Phù hợp desktop/mobile • Hoạt động không cần Internet sau khi tải các tệp.',W-867,11,DEEP,16)
 # theory
 top_rect(c,40,611,W-80,147,HexColor('#E8F1FB'),None,16)
 txt(c,62,629,'02  NGUYÊN LÝ KHOA HỌC',16,NAVY,True)
 txt(c,62,669,'BED = n · d · [1 + d / (α/β)] − K · max(0, T − Tₖ)',19,DEEP,True)
 txt(c,62,713,'Ví dụ bướu: 60 Gy / 30 phân liều, α/β = 10, T = 42, Tₖ = 28, K = 0,9',12,GRAY)
 top_rect(c,W-325,633,260,97,HexColor('#FFFFFF'),None,12)
 center_txt(c,W-195,644,'72,0 Gy₁₀  →  59,4 Gy₁₀',17,INDIGO,True)
 center_txt(c,W-195,687,'Giảm 12,6 Gy do tái sinh',11,GRAY)
 # modules
 txt(c,40,780,'03  BỐN MODULE TÍNH TOÁN',17,NAVY,True)
 line(c,40,811,W-40,811)
 module_names=[('01','BED & EQD2 CƠ BẢN','Đánh giá BED/EQD2 cho mô bướu và mô lành theo mô hình LQ, chưa xét tái sinh.',BLUE,'m1'),
  ('02','BED CÓ TÁI SINH','Tính BED trước và sau tái sinh; nhập riêng liều và thông số tái sinh của từng mô.',INDIGO,'m2'),
  ('03','CHUYỂN ĐỔI PHÁC ĐỒ','Tìm số phân liều hoặc liều mỗi lần mới sao cho BED theo giả định được bảo toàn.',GREEN,'m3'),
  ('04','MÔ PHỎNG SỬA SAI','Minh họa hiệu chỉnh phân liều và gián đoạn điều trị, có kết quả kiểm tra chéo.',ORANGE,'m4')]
 gap=20; cardw=(W-80-gap)/2;cardh=301
 for idx,(num,name,desc,color,mname) in enumerate(module_names):
  col=idx%2;row=idx//2;x=40+col*(cardw+gap);top=826+row*(cardh+16)
  top_rect(c,x,top,cardw,cardh,HexColor('#FFFFFF'),BORDER,15)
  top_rect(c,x+17,top+16,50,39,color,None,9)
  center_txt(c,x+42,top+23,num,15,HexColor('#FFFFFF'),True)
  txt(c,x+78,top+23,name,15,NAVY,True)
  imfile=BASE/'assets/previews'/f'{mname}.png'
  if imfile.exists():
   top_rect(c,x+16,top+67,cardw-32,179,PAPER,None,8)
   pic=Image.open(imfile).convert('RGB')
   pic=pic.crop((105,106,min(1330,pic.width),min(950,pic.height)))
   fit_img(c,_tmp_pic(pic,P/f'_poster_{mname}_tmp.jpg'),x+24,top+73,cardw-48,167,'contain')
  multiline(c,x+23,top+256,desc,cardw-46,10.5,GRAY,14,max_lines=2)
 # bottom QR / call to action
 bottom=826+2*(cardh+16)+6
 top_rect(c,40,bottom,W-80,168,NAVY,None,16)
 txt(c,61,bottom+15,'04  TRUY CẬP DỰ ÁN',15,HexColor('#FFFFFF'),True)
 multiline(c,61,bottom+47,'Quét mã để sử dụng website tương tác hoặc xem phiên bản poster trực tuyến.',355,12,HexColor('#D8ECFC'),19)
 txt(c,61,bottom+111,'GVHD: TS. Nguyễn Thị Cẩm Thu',11,HexColor('#A8D8FA'))
 txt(c,61,bottom+133,'Nhóm 4  |  Sinh học Bức xạ',11,HexColor('#A8D8FA'))
 qsize=123; left1=W-338;left2=W-181
 draw_qr_or_placeholder(c,qrweb if site_url else None,left1,bottom+14,qsize,'Website')
 draw_qr_or_placeholder(c,qrposter if site_url else None,left2,bottom+14,qsize,'Poster')
 center_txt(c,left1+qsize/2,bottom+141,'WEB',11,HexColor('#FFFFFF'),True)
 center_txt(c,left2+qsize/2,bottom+141,'POSTER',11,HexColor('#FFFFFF'),True)
 txt(c,40,H-45,'DỰ ÁN HỌC TẬP – KHÔNG DÙNG ĐỂ RA QUYẾT ĐỊNH ĐIỀU TRỊ.',10,GRAY,True)
 txt(c,40,H-28,'Mô hình LQ có các giới hạn; các thông số lâm sàng phải được xác minh từ tài liệu chuyên ngành.',9,GRAY)
 if not site_url:
  txt(c,40,H-12,'QR được tạo tự động bởi GitHub Actions khi xuất bản, hoặc chạy tools/finalize_poster.py --site-url ...',7.5,ORANGE)
 c.save()
 # raster high-resolution poster PNG
 doc=fitz.open(str(out));page=doc[0];pix=page.get_pixmap(matrix=fitz.Matrix(2.0,2.0),alpha=False)
 pix.save(str(P/'RadioBioCalc_Poster.png'))
 doc.close()
 for f in P.glob('_poster_*_tmp.jpg'):f.unlink()
 print('Poster:',out,round(out.stat().st_size/1024,1),'KiB; PNG', (P/'RadioBioCalc_Poster.png').stat().st_size)

def _tmp_pic(im,p):im.save(p,quality=88,optimize=True);return p

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--site-url',help='LIVE GitHub Pages URL, e.g. https://username.github.io/radiobiocalc/');ap.add_argument('--poster-url',help='Optional public PDF poster URL');args=ap.parse_args()
 if args.site_url:
  u=urlparse(args.site_url)
  if u.scheme!='https' or not u.netloc:ap.error('URL phải là https://... và truy cập được.')
 if args.poster_url:
  u=urlparse(args.poster_url)
  if u.scheme!='https' or not u.netloc:ap.error('Poster URL phải là https://...')
 make_pdf(args.site_url,args.poster_url)
if __name__=='__main__':main()
