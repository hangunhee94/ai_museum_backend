from http.client import ResponseNotReady
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from user.models import User as UserModel

from article.models import Article as ArticleModel
from article.models import Article as CommentModel

from article.serializers import ArticleSerializer
from article.serializers import CommentSerializer
from django.utils import timezone

# image trans pip
from PIL import Image
import io
import PIL
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile

# python 딥러닝 관련
import os
import glob
import shutil
from style_transfer.main import style_transfer

# file manage(관리) 쉽게 도움 주는 라이브러리 https://docs.djangoproject.com/en/3.0/topics/files/
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


# Create your views here.
class ArticleView(APIView):
    # 로그인 한 사용자의 게시글 목록 return
    # permission_classes =[permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        articles = ArticleModel.objects.all()
        today = timezone.now()
        serializer = ArticleSerializer(articles, many=True).data

        # articles = ArticleModel.objects.filter(
        #     exposure_start_date__lte = today,
        #     exposure_end_date__gte = today,    
        # ).order_by("-id")

        articles = ArticleModel.objects.all()

        return Response(serializer, status=status.HTTP_200_OK)
    
    def post(self, request):

        # user check
        request.data['user'] = request.user.id

        # user_id = request.data['user']

        content = request.data.get('content')
        file = request.FILES.get("image")
        number = request.data.get("number", "5")
        article = ArticleModel.objects.all()
        # print(file)
        # print(number)

        # if len(content) <= 5:
        #     return Response({"error": "내용은 5자 이상 작성해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 이미지 업로드를 위한 임시 폴더 생성 : style_transfer/input
        default_storage.save('./input/input_img.jpg', ContentFile(file.read()))
        
        # 선택 모델의 목록 1 ~ 9
        model = ['style_transfer/models/composition_vii.t7',
                 'style_transfer/models/la_muse.t7',
                 'style_transfer/models/starry_night.t7',
                 'style_transfer/models/the_wave.t7',
                 'style_transfer/models/candy.t7',
                 'style_transfer/models/feathers.t7',
                 'style_transfer/models/mosaic.t7',
                 'style_transfer/models/the_scream.t7',
                 'style_transfer/models/udnie.t7'
                 ]

        # model list select
        model_number = model[int(number)]
        # print(model[int(number)])

        # model learning
        style_transfer(model_number)

        # clear learning afterwards upload image delete
        shutil.rmtree('./style_transfer/input/')

        # ./style_transfer/output/* get folder_name_list
        list_of_files = glob.glob('./style_transfer/output/*')  # * means all if need specific format then *.csv
        # print(list_of_files)

        # ./style_transfer/output/* in get new file
        # get select image root : ./style_transfer/output/20220705-110621.jpg
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)

        # # get file name : 20220705-110621.jpg
        # result_img = os.path.basename(latest_file)

        # print(request.data)

        # InMemoryUploadedFile 변환
        img_io = io.BytesIO()
        print(img_io)
        img = Image.open(latest_file)
        print(img)
        # img_ext = list(os.path.splitext(img.filename))[-1]
        img_ext = os.path.basename(latest_file)
        print(img_ext)
        # percent = (basewidth / float(img.size[0]))
        # hsize = int(float(img.size[1]) * percent)
        # img = img.resize((basewidth, hsize),PIL.Image.ANTIALIAS)
        img.save(img_io, format="jpeg")
            
        new_pic = InMemoryUploadedFile(img_io, 
                'ImageField',
                img_ext,
                'jpeg',
                sys.getsizeof(img_io), None)

        # print(new_pic)
        # ArticleModel.objects.filter(image="*").update(new_pic)

        request.data['image'] = new_pic

        # request.data 하드코딩 덮어쓰기
        ArticleModel.objects.create(user=UserModel.objects.get(id=1), image=f'output/{new_pic}', content=content)
        print('OK')

        return Response({"message":"글 작성 완료"})

        # serializer 사용 불가..
        # serializer = ArticleSerializer(data=article_data)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({"message":"글 작성 완료"})
        # else:
        #     os.remove(latest_file)
        #     print(serializer.errors)
        #     return Response({"message":f'${serializer.errors}'}, 400)
        
   # 게시글 수정
    def put(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
        article_serializer = ArticleSerializer(
            article, data=request.data, partial=True)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request):
        return Response({'message': '삭제 성공!'})

     
# class ArticleView(APIView):

#     def get(self, request):
#         user = request.user.id
#         articles = Article.objects.filter(user_id=user)
#         articles = ArticleSerializer(articles, many=True).data

#         return Response(articles, status=status.HTTP_200_OK)
    
    
#     def post(self, request):
#         content = request.data.get("content", "")
#         file = request.data.get("file")
#         # 사용자가 선택한 모델의 넘버
#         number = request.data.get("number", "")

#         # 이미지 업로드를 위한 임시 폴더 생성 : style_transfer/input
#         default_storage.save('style_transfer/input/input_img.jpg', ContentFile(file.read()))

#         # 선택 모델의 목록 1 ~ 9
#         model = ['style_transfer/models/composition_vii.t7',
#                  'style_transfer/models/la_muse.t7',
#                  'style_transfer/models/starry_night.t7',
#                  'style_transfer/models/the_wave.t7',
#                  'style_transfer/models/candy.t7',
#                  'style_transfer/models/feathers.t7',
#                  'style_transfer/models/mosaic.t7',
#                  'style_transfer/models/the_scream.t7',
#                  'style_transfer/models/udnie.t7'
#                  ]

#         model_number = model[int(number)]
#         style_transfer(model_number)

#         shutil.rmtree('style_transfer/input/')

#         list_of_files = glob.glob('style_transfer/output/*')  # * means all if need specific format then *.csv
#         latest_file = max(list_of_files, key=os.path.getctime)


#         user = request.user.id
#         article = {'user': user, 'content': content, 'result_img': {file}}
#         # article = {'user': user, 'title': title, 'img_url': latest_file}
#         article_serializer = ArticleSerializer(data=article)
#         if article_serializer.is_valid():
#             article_serializer.save()
#             return Response(status=status.HTTP_200_OK)

#         else:
#             os.remove(latest_file)
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# '''
# 수정 및 삭제 로직 : 출처 내배캠 2기 5조

#     def put(self, request, article_id):
#         try:
#             article = Article.objects.get(id=article_id)
#         except Article.DoesNotExist:
#             return Response({"error": "존재하지 않는 게시물입니다."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         # article_serializer = ArticleSerializer(article, data=request.data, partial=True)
#         # article_serializer.is_valid(raise_exception=True)
#         # article_serializer.save()

#         return Response({"message": "put method"}, status=status.HTTP_200_OK)

#     def delete(self, request, article_id):
#         user = request.user.id
#         article = Article.objects.filter(id=article_id)
#         print(user)
#         print(article[0].user_id)
#         if user == article[0].user_id:
#             article.delete()
#             os.remove(article[0].img_url)
#             return Response({"message": "게시물이 삭제되었습니다."}, status=status.HTTP_200_OK)

#         return Response({"message": "실패."}, status=status.HTTP_400_BAD_REQUEST)
# '''



# '''
# 마이페이지 포스팅 조회
# '''

# class ArticleMyGalleryView(APIView):

#     def get(self, request):
#         user = request.user.id
#         articles = Article.objects.filter(user_id=user)
#         articles = ArticleSerializer(articles, many=True).data

#         return Response(articles, status=status.HTTP_200_OK)

#     def delete(self, request, article_id):
#         user = request.user.id
#         article = Article.objects.filter(id=article_id)
#         print(user)
#         print(article[0].user_id)
#         if user == article[0].user_id:
#             article.delete()
#             os.remove(article[0].img_url)
#             return Response({"message": "게시물이 삭제되었습니다."}, status=status.HTTP_200_OK)

#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

    

class CommentView(APIView):
    # 댓글 조회
    def get(self, request, article_id):
        comment = CommentModel.objects.filter(article=article_id)
        serialized_data = CommentSerializer(
            comment, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    # 댓글 작성
    def post(self, request, article_id):
        request.data["user"] = request.user.id
        request.data["article"] = article_id
        comment_serializer = CommentSerializer(data=request.data)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(comment_serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # 업데이트
    def put(self, request, comment_id):
        comment = CommentModel.objects.get(id=comment_id)
        comment_serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(comment_serializer.error, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def delete(self, request, comment_id):
        comment = CommentModel.objects.get(id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_200_OK)


class LikeView(APIView):
    def post(self, request, article_id):
        user = request.user
        article = ArticleModel.objects.get(id=article_id)
        likes = article.likes.all()
        like_lists = []
        for like in likes:
            like_lists.append(like.id)

        if user.id in like_lists:
            article.likes.remove(user)
            return Response({'message': '취소'})
        else:
            article.likes.add(user)
            return Response({'message': '좋아요'})