import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
import {withStyles} from '@material-ui/core/styles';
import Camera, { FACING_MODES } from 'react-html5-camera-photo';
import 'react-html5-camera-photo/build/css/index.css'


const styles = theme => ({
    root: theme.mixins.gutters({
        paddingTop: 16,
        paddingBottom: 16,
        marginTop: theme.spacing.unit * 3,
    }),
    container: {
        display: 'flex',
        flexWrap: 'wrap',
        flexDirection: "column",
        margin: "auto",
        maxWidth: "200px"
    },
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
        width: 200,
    },
    menu: {
        width: 200,
    },
});


class CardCapture extends Component {

    state = {};

    static propTypes = {
        onCapture: PropTypes.func.isRequired,
    };

    render() {
        const {classes} = this.props;

        return (
            <Paper className={classes.root}>
                <Camera
                    onTakePhoto={this.props.onCapture}
                    idealFacingMode={FACING_MODES.ENVIRONMENT}
                    isImageMirror={false}
                />
            </Paper>
        )
    }
}

export default withStyles(styles)(CardCapture);