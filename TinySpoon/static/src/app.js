var React = require('react');
var ReactDOM = require('react-dom');

//容器
var BoxWrap = React.createClass({
    render: function(){
        return <div className='content_box'>
                    <div className='small_title'>{this.props.title}</div>
                    <div>{this.props.children}</div>
               </div>
    }
});

//描述
var DesWrap = React.createClass({
    render: function(){
        return <BoxWrap title={this.props.title}>
                    <p className="des">{this.props.des}</p>
               </BoxWrap>
                
    }
});

//大标题
var HeadlineWrap = React.createClass({
    render: function(){
        return <div className='big_title'>{this.props.name}</div>
    }
});

//图片
var ImageWrap = React.createClass({
    render: function(){
        return  <div className='content_box'>
                   <HeadlineWrap name='小黄瓜燕麦煎饼'/>
                   <img className="banner" src='assets/images/10.jpg' />
                </div>
    }
});

//标签
var data = [
  {name: "小黄瓜", company: "2根"},
  {name: "小黄", company: "5根"},
  {name: "盐", company: "5根"}
];

var LabelWrap = React.createClass({
    render: function(){
        var items = this.props.data.map(function(item){
            return (
                <div className="label">{item.name}</div>
            )
        });
        return <BoxWrap title={this.props.title}>
                    <div className="label_box">
                        {items}
                    </div>
               </BoxWrap>
    }
});

//列表
var data = [
  {name: "小黄瓜", company: "2根"},
  {name: "小黄", company: "5根"},
  {name: "盐", company: "5根"}
];

var ListWrap = React.createClass({
    render: function(){
        var items = this.props.data.map(function(item){
            return (
                <tr className='row'>
                    <td className='rank left'>{item.name}</td>
                    <td className='rank right'>{item.company}</td>
                </tr>
            );
        });
        return (
            <BoxWrap title={this.props.title}>
                <table className='list'>
                    {items}
                </table>
            </BoxWrap>
        );
    }
});

//图文组件
var step =[
  {url: "assets/images/1.jpg", des: "材料：鸡蛋，黄瓜，洋葱酥（宜家有售），燕麦和面粉",seq:1},
  {url: "assets/images/1.jpg", des: "材料：鸡蛋，黄瓜，洋葱酥（宜家有售），燕麦和面粉",seq:2},
  {seq:4,url: "assets/images/1.jpg", des: "材料：鸡蛋，黄瓜，洋葱酥（宜家有售），燕麦和面粉"}
];
var StepWrap = React.createClass({
    render: function(){
        var items = this.props.data.map(function(item){
            return (
                 <tr className="img_des">
                    <td><img className="img" src={item.url}/></td>
                    <td className="des"><span>{item.seq}</span>{item.des}</td>
                 </tr>
            )
        });
        return (
            <BoxWrap title={this.props.title}>
                <table className="img_des_box">
                    {items}
                </table>
            </BoxWrap>
        )
    }
});

 
//ajax
var GetData = React.createClass({

    componentDidMount: function(){

        $.ajax({
            url:this.props.source,
            dataType:'jsonp',
            jsonp: "callback",
            success:function(data){
                data = JSON.parse(data);
                this.setState({data: data});
            }.bind(this),
            error:function(xhr,status,err){
                 console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    componentWillUnmount: function(){
        this.serverRequest.abort();
    },
    render:function(){
        return (
            <div></div>
        )
    }



});

ReactDOM.render(
  <GetData source="http://218.240.151.115:8081/api/recipes/112/" />,
  document.getElementById('data')
);




ReactDOM.render(
    <ImageWrap/>,
    document.getElementById('image')
);
ReactDOM.render(
    <LabelWrap data={data}/>,
    document.getElementById('label')
);
ReactDOM.render(
    <DesWrap title='简介' des='早餐我很喜欢做这样的煎饼来吃，配一杯豆浆或者薏米糊，一份水果，营养就很全面了。小黄瓜香味清新，燕麦健康，加上非常少油的煎制，好吃营养无负担！燕麦可以换成全麦粉或者其他杂粮粉哦！'/>,
    document.getElementById('synopsis')
);
ReactDOM.render(
    <ListWrap title='用料' data={data}/>,
    document.getElementById('material')
);
ReactDOM.render(
    <StepWrap title='做法' data={step}/>,
    document.getElementById('step')
);
ReactDOM.render(
    <DesWrap title='营养小贴士' des='我平时炒菜的标配就是平底锅和一双无漆的筷子。平底锅炒菜即使用很少的油，也不会有炒不开，糊锅的情况发生。'/>,
    document.getElementById('prompt')
);


