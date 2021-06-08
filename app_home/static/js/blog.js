function previewImage() {
            var avatar = document.getElementById("id_avatar").files;
            if (avatar.length > 0) {
                var fileReader = new FileReader();

                fileReader.onload = function (event) {
                    document.getElementById("avatar_preview").style.backgroundImage = 'url(' + event.target.result + ')';
                };
                fileReader.readAsDataURL(avatar[0]);
            }
        }