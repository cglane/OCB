var gulp = require('gulp'),
less = require('gulp-less'),
sourcemaps = require('gulp-sourcemaps'),
less_task = function() {
    gulp.src('sandbox/static/oscar/less/*.less')
        .pipe(less({
            includePaths: [
                'sandbox/static/less/',
            ],
            outputStyle: null,
        }))
        .pipe(sourcemaps.write('sandbox/static/oscar/css/'))
        .pipe(gulp.dest('sandbox/static/oscar/css/'));
};

gulp.task('less', less_task);