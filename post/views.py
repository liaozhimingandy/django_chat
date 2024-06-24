import uuid
from copy import deepcopy

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from post.lib.utils import get_uploaded_file_md5
from post.models import Post, Like, Comment, Image
from post.serializers import PostSerializer, CommentSerializer, ImageUploadSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    自定义分页器
    """
    page_size = 10  # 默认每页显示的记录数
    page_size_query_param = 'page_size'  # 允许客户端通过查询参数指定每页大小
    max_page_size = 100  # 客户端可以请求的最大记录数

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'data': data
        })


class LikeViewSet(viewsets.ViewSet):
    """
    点赞相关操作
    """

    def list(self, request):
        return Response(data={'message': 'likes'})

    @action(detail=False, methods=['post'], url_path='(?P<post_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-['
                                                     r'0-9a-fA-F]{4}-[0-9a-fA-F]{12})')
    def create_like(self, request, post_id: uuid):
        """
        创建点赞
        :param request:
        :param post_id: 帖子ID <br>
        :return:
        """
        payload = request.data
        Like(post_id=post_id, account_id=payload["account_id"]).save()
        count_like = Like.objects.filter(post_id=post_id).count()
        data = {"count": count_like, "is_like": True}
        return Response(data=data)

    @action(detail=False, methods=['delete'], url_path='(?P<post_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-['
                                                       r'0-9a-fA-F]{4}-[0-9a-fA-F]{12})/(?P<account_id>['
                                                       r'0-9a-zA-Z_]+)')
    def delete_like(self, request, post_id: uuid, account_id: str):
        """
        取消点赞
        :param request:
        :param post_id:
        :param account_id:
        :return:
        """
        Like.objects.filter(post_id=post_id, account_id=account_id).delete()
        count_like = Like.objects.filter(post_id=post_id).count()
        return Response(data={"count": count_like, "is_like": False})

    @action(detail=False, methods=['GET'], url_path='(?P<post_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-['
                                                    r'0-9a-fA-F]{4}-[0-9a-fA-F]{12})/(?P<account_id>['
                                                    r'0-9a-zA-Z_]+)/count')
    def get_likes(self, request, post_id: uuid, account_id: str):
        """
        获取点赞数量
        :param request:
        :param post_id:
        :param account_id:
        :return:
        """
        count_like = Like.objects.filter(post_id=post_id).count()
        is_like = Like.objects.filter(post_id=post_id, account_id=account_id).exists()
        return Response(data={"count": count_like, "is_like": is_like})


class PostViewSet(viewsets.ModelViewSet):
    """
    帖子相关操作
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "post_id"

    @action(methods=['get'], detail=False)
    def lasted(self, request, format=None):
        """
        获取最近十条数据 <br>
        :param request: <br>
        :param format: <br>
        :return: <br>
        """
        posts = Post.objects.order_by('-id')[:10]
        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    """
    评论相关操作
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    ordering_fields = ('-id',)
    lookup_field = 'comment_id'

    @action(detail=False, methods=['get'], url_path=r'posts/(?P<post_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-['
                                                    r'0-9a-fA-F]{4}-[0-9a-fA-F]{12})/count')
    def get_comment_count(self, request, post_id: uuid):
        """
        获取指定帖子的评论数<br>
        :param request:
        :param post_id: 帖子id <br>
        :return: <br>
        """
        _count = Comment.objects.filter(post_id=post_id).count()
        return Response(data={'count': _count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path=r'posts/(?P<post_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-['
                                                    r'0-9a-fA-F]{4}-[0-9a-fA-F]{12})')
    def get_comments_by_post_id(self, request, post_id: uuid):
        queryset = Comment.objects.filter(post_id=post_id).all().order_by("-id")
        # 实例化分页类
        paginator = StandardResultsSetPagination()
        # 分页查询集
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            # 序列化分页后的数据
            serializer = CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        # 如果没有分页，则直接序列化整个查询集
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class UploadViewSet(viewsets.GenericViewSet):
    """
    文件上传接口
    """
    serializer_class = ImageUploadSerializer

    @action(detail=False, methods=['post'], url_path="image")
    def upload_image(self, request):
        """

        图片上传接口<br>

        :param request: 图片路径<br>
        :return: 图片模型对象<br>
        """
        data = request.data

        # 获取图片md5
        # image_copy = deepcopy(data['image']) if isinstance(data['image'], (InMemoryUploadedFile,)) else data['image']
        image_copy = deepcopy(data['image'])
        image_md5 = get_uploaded_file_md5(image_copy)

        # 如果存在则返回已有数据
        if Image.objects.filter(image_md5=image_md5).exists():
            image = Image.objects.get(image_md5=image_md5)
            serializer = self.get_serializer(image)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        try:
            data['image_md5'] = image_md5
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        # 未知错误，报服务器内部错误
        except (Exception,) as error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"detail": str(error)})
