function sendArticleComment(articleId) {
    var comment = $('#comment-text').val();
    var parentId = $('#parent_id').val();

    $.get('/articles/add-article-comment', {
        article_comment: comment,
        article_id: articleId,
        parent_id: parentId,
    }).then(res => {
        $('#comment_area').html(res);
        $('#comment-text').val('');
        $('#parent_id').val('');
        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: "smooth"});
        } else {
            document.getElementById('comment_area').scrollIntoView({behavior: "smooth"});

        }
    })
}

function sendProductComment(productId) {
    var comment = $('#comment-text').val();
    var parentId = $('#parent_id').val();

    $.get('/products/add-product-comment', {
        product_comment: comment,
        product_id: productId,
        parent_id: parentId,
    }).then(res => {
        $('#comment_area').html(res);
        $('#comment-text').val('');
        $('#parent_id').val('');
        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: "smooth"});
        } else {
            document.getElementById('comment_area').scrollIntoView({behavior: "smooth"});

        }
    })
}


function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"});

}


function filterProduct() {
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price)
    $('#end_price').val(end_price)
    $('#filter_form').submit()

}

function fillpage(page) {
    $('#page').val(page);
    $('#filter_form').submit();

}

function showLargeImage(imageSrc) {
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image_model').attr('href', imageSrc);

}


function addProductToOrder(productId) {
    let productCount = $('#product_count').val();
    if (productCount == null || productCount === 0) {
        productCount = 1
    }
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            confirmButtonText: 'باشه',
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_authorized') {
                window.location.href = '/register';
            }
        });
    });
}

function removeOrderDetail(detailId) {
    $.get('/userpanel/remove-order-detail?detail_id=' + detailId).then(res => {
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            confirmButtonText: 'باشه',
        });
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
            console.log('Successfully removed')
        }
    });
}

function changeOrderDetailCount(detailId, state) {
    console.log(detailId, state);

    $.get('/userpanel/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
            console.log('Successfully removed')
        }
    });
}
