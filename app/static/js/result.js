/**
 * Created by fruit on 2016/11/21.
 */

$(function () {
    $(".searchPart a").on('click', function () {
        var id = $(this).attr('id')
        $('.' + id).removeClass('isHidden')
        alert(id)

    })
})