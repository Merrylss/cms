var testEditor;

$(function() {
    testEditor = editormd("test-editormd", {
        width   : "100%",
        height  : 800,
        syncScrolling : "single",
        path    : "./js/lib/editor.md-master/lib/"
    });

    /*
    // or
    testEditor = editormd({
        id      : "test-editormd",
        width   : "90%",
        height  : 640,
        path    : "../lib/"
    });
    */
    //富文本框对象
    var ue = UE.getEditor('editor');
    // 选项卡
    var _titles = $(".t");
    console.log(_titles.size());
    var _contents = $(".c1");

    for(var i=0;i<_titles.size();i++){
        _titles[i].index = i;
        console.log(_titles[i]);

        $(_titles[i]).click(function () {
            for(var j=0;j<_contents.size();j++){
                console.log(_contents[j]);
                _contents[j].style.display = 'none';
            }
            _contents[this.index].style.display = 'block';
        })
    }
});



