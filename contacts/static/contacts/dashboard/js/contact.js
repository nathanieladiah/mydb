document.addEventListener('DOMContentLoaded', () => {

	document.querySelectorAll('button.edit-note').forEach(button => {
		button.onclick = () => {
			const noteId = button.dataset.note;
			editNote(noteId);
		}
	});

	document.querySelectorAll('button.delete-note').forEach(button => {
		button.onclick = () => {
			const noteId = button.dataset.note;
			deleteNote(noteId);
		}
	});

	document.querySelectorAll('button.edit-interaction').forEach(button => {
		button.onclick = () => {
			const interactionId= button.dataset.interaction;
			editInteraction(interactionId);
		}
	});

	document.querySelectorAll('button.delete-interaction').forEach(button => {
		button.onclick = () => {
			const interactionId = button.dataset.interaction;
			deleteInteraction(interactionId);
		}
	})

	document.querySelector('#edit-about').addEventListener('click', editAbout);

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const editAbout = () => {
	// Hide the post and show an editor 
	const about = document.getElementById('about-detail');
	const editButton = document.getElementById('edit-about');
	const contactId = about.dataset.contact
	editButton.style.display = 'none';
	about.style.display = 'none';

	// fetch(`/contact/${contactId}/details/`)
	// .then(response => response.json())
	// .then(post => {
	// 	console.log(post);
	// })

	const editor = document.createElement('div');
	editor.classList.add('w-100');
	editor.id = 'about-editor'

	const body = document.createElement('textarea');
	body.classList.add('editor-body', 'w-100');
	body.innerHTML = about.innerHTML;
	body.id = 'new-about-text';
	editor.appendChild(body);

	const save = document.createElement('button');
	save.id = 'save-about';
	save.classList.add('btn', 'btn-primary', 'btn-sm', 'save-btn');
	save.innerHTML = 'Save';
	editor.appendChild(save);


	// need to attach the editor to the DOM
	document.querySelector('#profile-about').append(editor);

	// Eventhandler for click on save edit button
	save.addEventListener('click', () => {
		// A Post request to change the value of the post
		saveAboutEdit(editor, editButton, about, contactId, body);
		// Stop form from submitting
		return false;	
	});

}

const saveAboutEdit = (editor, editButton, about, contactId, body) => {
	const csrftoken = getCookie('csrftoken');
	const aboutBody = document.getElementById('new-about-text').value;
	// need to write an ajax request to update the correct contact's description
	fetch(`/contact/${contactId}/edit/`, {
		method: 'POST',
		body: JSON.stringify({
			description: aboutBody
		}),
		headers: {'X-CSRFToken': csrftoken}
	})
	.then(response => response.json())
	.then(result => {
		if (result.error) {
			alert(result.error);
			return
		} else {
			console.log(about.innerHTML, editButton.innerHTML);
			editor.style.display = 'none';
			about.innerHTML = aboutBody;
			// about.innerHTML = body;
			about.style.display = 'block';
			editButton.style.display = 'block';
		}
	});
}


function editNote(note_id) {
	// Hide the post and show an editor 

	const noteItem = document.querySelector(`#note-${note_id}-body`);
	const noteActions = document.querySelector(`#note-${note_id}-actions`);
	noteActions.style.display = 'none';
	noteItem.style.display = 'none';

	fetch(`/note/${note_id}/`)
	.then(response => response.json())
	.then(note => {

		const editor = document.createElement('div');
		editor.classList.add('post-editor', 'w-100');
		editor.id = `edit-note-${note.id}`;

		const body = document.createElement('textarea');
		body.classList.add('editor-body', 'w-100');
		body.innerHTML = note.body;
		body.id = `edit-${note.id}`;
		editor.appendChild(body);

		const save = document.createElement('button');
		save.id = `save-note-${note.id}`;
		save.classList.add('btn', 'btn-primary', 'save-btn');
		save.innerHTML = 'Save';
		editor.appendChild(save);


		// need to attach the editor to the DOM
		document.querySelector(`#note-${note_id}`).append(editor);

		// Eventhandler for click on edit button
		save.addEventListener('click', () => {
			// A Post request to change the value of the post
			saveNoteEdit(note, editor, noteItem, noteActions);
			// Stop form from submitting
			return false;	
		});

	})
}


const saveNoteEdit = (note, editor, noteItem, noteActions) => {
	const csrftoken = getCookie('csrftoken');
	const noteBody = document.querySelector(`#edit-${note.id}`).value;
	fetch(`/note/${note.id}/edit`, {
		method: 'POST',
		body: JSON.stringify({
			body: noteBody
		}),
		headers: {'X-CSRFToken': csrftoken}
	})
	.then(response => response.json())
	.then(result => {
		if (result.error) {
			alert(result.error);
			return 
		} else {
			editor.style.display = 'none';
			noteItem.innerHTML = noteBody;
			noteItem.style.display = 'block';
			noteActions.style.display = 'inline';
		}
	})
}

const deleteNote = (noteId) => {
	const csrftoken = getCookie('csrftoken');
	const noteItem = document.getElementById(`note-${noteId}`);
	fetch(`/note/${noteId}/delete`, {
		method: 'POST',
		headers: {'X-CSRFToken': csrftoken}
	})
	.then(response => response.json())
	.then(result => {
		if (result.error) {
			alert(result.error);
			return
		} else {
			noteItem.style.display = 'none';
		}
	})
}


const editInteraction= (interactionId) => {

	// Hide the post and show an editor 
	const item = document.querySelector(`#interaction-${interactionId}-body`);
	const actions = document.querySelector(`#interaction-${interactionId}-actions`);
	actions.style.display = 'none';
	item.style.display = 'none';

	fetch(`/interaction/${interactionId}/`)
	.then(response => response.json())
	.then(interaction => {

		const editor = document.createElement('div');
		editor.classList.add('post-editor', 'w-100');
		editor.id = `edit-interaction-${interaction.id}`;

		const body = document.createElement('textarea');
		body.classList.add('editor-body', 'w-100');
		body.innerHTML = interaction.body;
		body.id = `edit-${interaction.id}`;
		editor.appendChild(body);

		const save = document.createElement('button');
		save.id = `save-interaction-${interaction.id}`;
		save.classList.add('btn', 'btn-primary', 'save-btn');
		save.innerHTML = 'Save';
		editor.appendChild(save);


		// need to attach the editor to the DOM
		document.querySelector(`#interaction-${interactionId}`).append(editor);

		// Eventhandler for click on edit button
		save.addEventListener('click', () => {
			// A Post request to change the value of the post
			saveInteractionEdit(interaction, editor, item, actions);
			// Stop form from submitting
			return false;	
		});

	})
}

const saveInteractionEdit = (interaction, editor, item, actions) => {
	const csrftoken = getCookie('csrftoken');
	const interactionBody = document.querySelector(`#edit-${interaction.id}`).value;
	fetch(`/interaction/${interaction.id}/edit`, {
		method: 'POST',
		body: JSON.stringify({
			body: interactionBody
		}),
		headers: {'X-CSRFToken': csrftoken}
	})
	.then(response => response.json())
	.then(result => {
		if (result.error) {
			alert(result.error);
			return 
		} else {
			editor.style.display = 'none';
			item.innerHTML = interactionBody;
			item.style.display = 'block';
			actions.style.display = 'inline';
		}
	})
}

const deleteInteraction= (interactionId) => {
	const csrftoken = getCookie('csrftoken');
	const item = document.getElementById(`interaction-${interactionId}`);
	fetch(`/interaction/${interactionId}/delete`, {
		method: 'POST',
		headers: {'X-CSRFToken': csrftoken}
	})
	.then(response => response.json())
	.then(result => {
		if (result.error) {
			alert(result.error);
			return
		} else {
			item.style.display = 'none';
		}
	})
}
