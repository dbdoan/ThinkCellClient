import { TypeAnimation } from 'react-type-animation';
import { useRef } from 'react';

const CURSOR_CLASS_NAME = 'custom-type-animation-cursor';

const IntroComponent = () => {
    const ref = useRef(null);

    const showCursorAnimation = (show) => {
        if (!ref.current) return;
        if (show) {
            ref.current.classList.add(CURSOR_CLASS_NAME);
        } else {
            ref.current.classList.remove(CURSOR_CLASS_NAME);
        }

    };

    return (
        <>
            <TypeAnimation
                ref={ref}
                cursor={false}
                className={CURSOR_CLASS_NAME}
                sequence={[
                    'Introducing Thinkcell Panel',
                    4000,
                    () => showCursorAnimation(false)
                ]}
                wrapper="span"
                speed={50}
                style={{ 
                    fontFamily: 'system-ui, Avenir, Helvetica, Arial, sans-serif',
                    fontSize: '3.2em', 
                    fontWeight: 'bold',
                    lineHeight: '1.1', 
                    display: 'inline-block'
                }}
            />
        </>
    );
};

export default IntroComponent;