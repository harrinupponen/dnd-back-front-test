let base64Image;
        $('#image-selector').change(function() {
            let reader = new FileReader();
            reader.onload = function(e) {
                let dataURL = reader.result;
                $('#selected-image').attr('src', dataURL);
                base64Image = dataURL.replace('data:image/png;base64,', '').replace('data:image/jpeg;base64,', '');
                //console.log(base64Image);
            }
            reader.readAsDataURL($('#image-selector')[0].files[0]);
            $('#barbarian-prediction').text('');
            $('#bard-prediction').text('');
            $('#cleric-prediction').text('');
            $('#druid-prediction').text('');
            $('#fighter-prediction').text('');
            $('#mage-prediction').text('');
            $('#monk-prediction').text('');
            $('#paladin-prediction').text('');
            $('#rogue-prediction').text('');
            $('#sorcerer-prediction').text('');
            $('#warlock-prediction').text('');
            $('#wizard-prediction').text('');
        });

        $('#predict-button').click(function(event) {
            let message = {
                image: base64Image
            }
            //console.log(message);

            $.get('http://localhost:5000/result', function() {
                console.log('GETTEM!');
            });
            $.post('http://localhost:5000/result', JSON.stringify(message),
            function(response) {
                $('#barbarian-prediction').text((100 * (response.prediction.barbarian)).toFixed(2) + '%');
                $('#bard-prediction').text((100 * (response.prediction.bard)).toFixed(2) + '%');
                $('#cleric-prediction').text((100 * (response.prediction.cleric)).toFixed(2) + '%');
                $('#druid-prediction').text((100 * (response.prediction.druid)).toFixed(2) + '%');
                $('#fighter-prediction').text((100 * (response.prediction.fighter)).toFixed(2) + '%');
                $('#mage-prediction').text((100 * (response.prediction.mage)).toFixed(2) + '%');
                $('#monk-prediction').text((100 * (response.prediction.monk)).toFixed(2) + '%');
                $('#paladin-prediction').text((100 * (response.prediction.paladin)).toFixed(2) + '%');
                $('#rogue-prediction').text((100 * (response.prediction.rogue)).toFixed(2) + '%');
                $('#sorcerer-prediction').text((100 * (response.prediction.sorcerer)).toFixed(2) + '%');
                $('#warlock-prediction').text((100 * (response.prediction.warlock)).toFixed(2) + '%');
                $('#wizard-prediction').text((100 * (response.prediction.wizard)).toFixed(2) + '%');

                console.log(response);
                
            });
            // $.get('http://localhost:5000/result', function() {
            //     console.log('GETTEM!');
            // });
        });