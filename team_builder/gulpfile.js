const gulp = require('gulp')
const mochaPhantomJS = require('gulp-mocha-phantomjs')

gulp.task('test', function () {
    return gulp
    .src('test/utilities_test/*.html')
    .pipe(mochaPhantomJS())
})