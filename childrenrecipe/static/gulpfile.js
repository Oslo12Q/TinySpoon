var gulp = require('gulp');
var connect = require('gulp-connect');
var less = require('gulp-less');
var minifyCss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var babelify = require('babelify');
var source = require('vinyl-source-stream');
var browserify = require('browserify');


gulp.task('connect',function(cb){
    connect.server({
        root:'.',
        livereload:true,
        port:1500
    });
    cb();
});

//编译less文件，压缩css文件
gulp.task('less',function(){
    return gulp.src('./assets/less/*.less')
        .pipe(less())
        .pipe(gulp.dest('./assets/css'))
        .pipe(minifyCss())
        .pipe(rename({extname:'.min.css'}))
        .pipe(gulp.dest('./assets/css'));
});

//将模块化js脚本打包成一个js文件
gulp.task('browserify',function(){
    return browserify('./src/app.js',{debug:true})
    .transform(babelify.configure({presets: ['es2015', 'react']}))
    .bundle()
    .pipe(source('bundle.js'))
    .pipe(rename({basename:'app', extname: '.js'}))
    .pipe(gulp.dest('./assets/js/'));
});


//压缩js脚本
gulp.task('uglify',['browserify'],function(){
    return gulp.src('./assets/js/*.js')
    //.pipe(ngmin({dynamic: false}))
    .pipe(uglify({outSourceMap: true}))
    .pipe(rename({extname: '.min.js'}))
    .pipe(gulp.dest('./assets/js/'));
});

//监听html less js
gulp.task('reload', ['less', 'browserify'], function(){
	return gulp.src(['./*.html', './assets/**/*', './src/**/*'])
		.pipe(connect.reload());
});

gulp.task('watch',['watch-html','watch-less','watch-js']);

gulp.task('watch-html',function(){
    gulp.watch(['./*.html'],['reload']);
});

gulp.task('watch-less',function(){
    gulp.watch(['./assets/less/*.less'],['reload']);
});

gulp.task('watch-js',function(){
    gulp.watch(['./src/**/*.js'],['reload']);
});

gulp.task('compile',['less','browserify']);
gulp.task('default',['compile', 'connect','watch']);
gulp.task('port',['uglify','compile','watch']);
