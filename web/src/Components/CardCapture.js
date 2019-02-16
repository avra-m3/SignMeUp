import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import {withStyles} from '@material-ui/core/styles';
import Camera, {FACING_MODES} from 'react-html5-camera-photo';
import 'react-html5-camera-photo/build/css/index.css'


const styles = theme => ({
    root: theme.mixins.gutters({
        paddingTop: 16,
        paddingBottom: 16,
        marginTop: theme.spacing.unit * 3,
    }),

});


class CardCapture extends Component {

    state = {};

    static propTypes = {
        onCapture: PropTypes.func.isRequired,
        show: PropTypes.bool.isRequired
    };

    render() {
        const {classes} = this.props;
        const hiddenStyle = {
            display: "none"
        };
        return (
            <div style={this.props.show ? {} : hiddenStyle}>
                <Camera
                    onTakePhoto={this.props.onCapture}
                    idealFacingMode={FACING_MODES.ENVIRONMENT}
                    isImageMirror={false}
                    isMaxResolution={true}
                />
            </div>
        )
    }
}

export default withStyles(styles)(CardCapture);