var gulp = require('gulp');

gulp.task('watch', function() {
    var watch = require('gulp-watch');

    gulp.watch('sandbox/static/oscar/less/**/*.less', ['less']);
});