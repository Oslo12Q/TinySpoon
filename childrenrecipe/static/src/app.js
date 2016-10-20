var React = require('react');
var ReactDOM = require('react-dom');

//容器
var BoxWrap = React.createClass({
    render: function(){
        return <div>
                    <div className={'small_title border_box '+this.props.controller}>{this.props.title}</div>
                    <div>{this.props.children}</div>
               </div>
    }
});

//描述
var DesWrap = React.createClass({
    render: function(){
        return <BoxWrap controller={this.props.controller} title={this.props.title}>
                    <p className="des">{this.props.des}</p>
               </BoxWrap>
                
    }
});

//图片
var ImageWrap = React.createClass({
    render: function(){
        return  <div>
                   <div className='big_title pc_controller'>{this.props.reqData.name}</div>
                   <img className="banner" src={this.props.reqData.exihibitpic} />
                   <div className='big_title app_controller'>{this.props.reqData.name}</div>
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
        return <BoxWrap controller={this.props.controller} title={this.props.title}>
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
                    <td className='rank'>{item.name}</td>
                    <td className='rank'>{item.portion}</td>
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
                <li className="des_li" key={item.id}>
                    <div className='num app_controller'>{item.seq}</div>
                    <div className="app_controller">
                        <div><img  className="img" src={item.image} /></div>
                        <p className='step_des'>{item.describe}</p>
                    </div>
                    <div className='pc_controller'>
                        <div className='left'><img className="img" src={item.image}/></div>
                        <div className="des"><span className='num'>{item.seq}</span>{item.describe}</div>
                    </div>
                    
                </li>   
            )
        });
        return (
            <BoxWrap title={this.props.title}>
                <div className="img_des_box">
                    <ul className="img_des">
                        {items}
                    </ul>
                </div>
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
				<LabelWrap controller='pc_controller' title='标签' data={this.state.tagList}></LabelWrap>
				<DesWrap controller='pc_controller' title='简介' des={this.state.data.introduce}></DesWrap>
				<ListWrap title='用料' data={this.state.materialList}></ListWrap>
				<StepWrap title='做法' data={this.state.procedureList}></StepWrap>
				<DesWrap title='营养小贴士' des={this.state.data.tips}></DesWrap>
			</div>
        )
    }
    
});

//获取url参数
function getQueryString(name) { 
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
	var r = window.location.search.substr(1).match(reg); 
	if (r != null) return unescape(r[2]); return null; 
} 
var id = getQueryString('state');

//var requestURL = "http://caimiao.yijiayinong.com:8081/api/recipes/"+id;
var requestURL = 'http://218.240.151.115:8080/api/recipes/'+id;
//var requestURL = "http://localhost:1500/data.json";

ReactDOM.render(
  <GetData source={requestURL}/>,
  document.getElementById('data')
);


