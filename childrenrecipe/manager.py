# coding=utf-8
from django.db.models import Q

from childrenrecipe.models import Tag, Recipe, Category

AGE_CATEGORY_NAME = u"年龄"


#def create_category(name, is_tag=1, seq=0):
#    """
#    创建category
#    """
#    return Category.objects.create(
#        name=name,
#        is_tag=is_tag,
#        seq=seq,
#    )


#def create_tag(name, category_id, seq=1):
#    """
#    创建tag
#    """
#    return Tag.objects.create(
#        name=name,
#        category_id=category_id,
#        seq=seq,
#    )


#def get_tag_by_id(tag_id):
#    """
#    根据id查找tag
#    """
#    return Tag.objects.get(id=tag_id)


#def create_recipe(name, user, introduce="", tips="", tag_id_list=None):
#    """
#    创建recipe
#    """
#    recipe = Recipe.objects.create(
#        name=name,
#        user=user,
#        introduce=introduce,
#        tips=tips,
#    )
#    if tag_id_list is not None:
#        for tag_id in tag_id_list:
#            tag = get_tag_by_id(tag_id)
#            recipe.tag.add(tag)
#        recipe.save()
#    return recipe


def get_category_by_name(name):
    """
    :param name 类别的名字
    """
    return Category.objects.get(name=name)


def get_tag_queryset(tag_id_list=None, category=None):
    """
    根据参数获取tag
    1.tag_id_list是None的时候,直接反空queryset
    2.tag_id_list不为None的时候,根据参数返值
    :param tag_id_list tag id的数据形式
    :param category Category实例
    :return Tag queryset
    """
    query = Q()
    if tag_id_list is not None:
        query &= Q(id__in=tag_id_list)
        if category is not None:
            query &= Q(category=category)
        return Tag.objects.filter(query)
    return Tag.objects.none()


def get_recipe(tag_id_list=None, search=None):
    """
    根据参数获取recipe
    :param tag_id_list tag id的数据形式
    :param search 查询recipe的名字(模糊查询)
    """
    other_tag_query_set = None
    query = Q()
    if search:
        query &= Q(name__contains=search)
    # 获取年龄的分类
    age_category = get_category_by_name(AGE_CATEGORY_NAME)
    # 获取传入的tag里面跟年龄有关的
    age_tag_queryset = get_tag_queryset(tag_id_list, age_category)
    if age_tag_queryset:
        query &= Q(tag__in=age_tag_queryset)
    if tag_id_list is not None:
        other_tag_id_set = set(tag_id_list).difference(set(age_tag_queryset.values_list("id", flat=True)))
        other_tag_query_set = get_tag_queryset(list(other_tag_id_set))
    if other_tag_query_set:

        return Recipe.objects.filter(query).filter(tag__in=other_tag_query_set).distinct().order_by("-create_time")
    return Recipe.objects.filter(query).distinct().order_by("-create_time")

