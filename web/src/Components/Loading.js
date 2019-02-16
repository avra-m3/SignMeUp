import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import {withStyles} from '@material-ui/core/styles';
import LinearProgress from "../../node_modules/@material-ui/core/LinearProgress/LinearProgress";


const styles = theme => ({
    root: {
        display: 'flex',
        flexDirection: 'row',
    },
    progress: {
        flexGrow: 1,
    },
});


class CardCapture extends Component {

    state = {};

    static propTypes = {
        onCapture: PropTypes.func.isRequired,
    };

    render() {
        const {classes, registration} = this.props;

        return (
            <div className={classes.root}>
                <div className={classes.progress}>
                    <LinearProgress/>
                </div>
            </div>
        )
    }
}

export default withStyles(styles)(CardCapture);