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

//大标题
var HeadlineWrap = React.createClass({
    render: function(){
        return <div className='big_title'>{this.props.name}</div>
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

//图片
var ImageWrap = React.createClass({
    render: function(){
        return  <div className='content_box'>
                   <HeadlineWrap name={this.props.reqData.name}/>
                   <img className="banner" src={this.props.reqData.exihibitpic} />
                </div>
    }
});

//标签
var LabelWrap = React.createClass({
    render: function(){
		var data = [];
        var items = this.props.data.map(function(item){
            return (
                <div className="label" key={item.id}>{item.name}</div>
            )
        });
        return <BoxWrap title={this.props.title}>
                    <div className="label_box">
                        {items}
                    </div>
               </BoxWrap>
    }
});

//列表组件
var ListWrap = React.createClass({
    render: function(){
		var data = [];
        var items = this.props.data.map(function(item){
            return (
                <tr className='row' key={item.id}>
                    <td className='rank left'>{item.name}</td>
                    <td className='rank right'>{item.portion}</td>
                </tr>
            );
        });
        return (
            <BoxWrap title={this.props.title}>
                <table className='list'>
                    <tbody>
                        {items}
                    </tbody>
                </table>
            </BoxWrap>
        );
    }
});

//图文组件
var StepWrap = React.createClass({
    render: function(){
        var items = this.props.data.map(function(item){
            return (
                <tr className="img_des" key={item.id}>
                    <td><img className="img" src={item.image}/></td>
                    <td className="des"><span>{item.seq}</span>{item.describe}</td>
                </tr>   
            )
        });
        return (
            <BoxWrap title={this.props.title}>
                <table className="img_des_box">
                    <tbody>
                        {items}
                    </tbody>
                </table>
            </BoxWrap>
        )
    }
});

 
//ajax
var GetData = React.createClass({

	getInitialState:function(){
		return {
			data:'',
			tagList:[],
			materialList:[],
			procedureList:[]
		};
	},

    componentDidMount: function(){
        $.ajax({
            url:this.props.source,
            dataType:'json',
            jsonp: "callback",
            success:function(data){
                this.setState({
						data: data,
						tagList: data.tag,
						materialList: data.material,
						procedureList: data.procedure
					});
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
			<div>
				<ImageWrap reqData={this.state.data}></ImageWrap>
				<LabelWrap title='标签' data={this.state.tagList}></LabelWrap>
				<DesWrap title='简介' des={this.state.data.introduce}></DesWrap>
				<ListWrap title='用料' data={this.state.materialList}></ListWrap>
				<StepWrap title='做法' data={this.state.procedureList}></StepWrap>
				<DesWrap title='营养小贴士' des={this.state.data.tips}></DesWrap>
			</div>
        )
    }
});

//获取url参数
function getRequest(){
	var url = window.location.href;
	console.log(url);
}
getRequest();


var dataId = '';
var requestURL = "http://218.240.151.115:8081/api/recipes/158";

ReactDOM.render(
  <GetData source={requestURL}/>,
  document.getElementById('data')
);


