import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Camera, {FACING_MODES} from 'react-html5-camera-photo';
import 'react-html5-camera-photo/build/css/index.css'

class CardCapture extends Component {

    state = {};

    static propTypes = {
        onCapture: PropTypes.func.isRequired,
        show: PropTypes.bool.isRequired
    };

    render() {
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

export default CardCapture;