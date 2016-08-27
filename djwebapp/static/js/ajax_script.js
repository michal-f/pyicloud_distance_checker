$(document).ready(function () {
    var edited_unsaved = [];
    var start_values = [];
    var question_id = document.getElementById("question_id").value;
    var save_btn = $('#main_save_button');
    var question = $('#question_single');
    var dropdown = $('#question_dropdown');
    dropdown.val(question_id);

    function dark() {
        return $("#highcontrast").hasClass('dark');
    }

    /*JAVASCRIPT TO HTML CONNECTION LOADER & REFRESHER*/
    function reloadJavascript() {
        rowEditable();
        first_row_edition_event();
        $('.rowEdit').click(EditRow);
        $('.rowDelete').click(DeleteRow);
    }

    /* VERIFY POST DATA AND MAKE REQUEST */
    function ajaxPoster(action_type, value_string, choice_id) {
        if (!value_string) {
            popup("error", gettext("String parameter not valid!"), gettext("Post Error"));
        }
        var actions = ["ERROR", "add", "del", "voteAdd", "voteRem", "delete", "questionUpdate", "getChoices"];
        var bool = false;
        var no_confirm;
        var job;
        try {
            var id_temp = parseInt(question_id.trim());
            var id = id_temp.toString();
            if (actions.indexOf(action_type.trim().toString()) > 0) {
                if (action_type.trim().toString() == "delete") {
                    no_confirm = true;
                    job = "del";
                } else {
                    no_confirm = false;
                    job = action_type.trim().toString();
                }
            } else {
                var info = action_type.trim().toString() + "/length=" + action_type.length.toString();
                popup("error", gettext("POST action not found:") + info, gettext("ajax post handler"));
            }
            if (value_string.trim().length > 0 && typeof value_string == "string")
                var param = value_string.trim();
            else
                popup("error", gettext("String param not valid!"), gettext("ajax post handler"), 1500);
            if (job && id && param) {
                var data = {'id': id, 'action': job, 'value': param};
                bool = true;
            }
        } catch (err) {
            bool = false;
            swal("error", err.message, gettext("ajax post handler"));
        }
        if (bool) {
            function do_post() {
                $.ajax({
                    "type": "POST",
                    "dataType": "json",
                    "url": "/polls/ajax/",
                    "data": data,
                    "success": function (result) {
                        if (job == "add" && result["result"] == "dup") {
                            var current_row = $("#choice_table").children('tbody').children('tr').last();
                            current_row.remove();
                            popup("warning", gettext("Choice already in db. Unable to add."), gettext("Duplicates not allowed!"));
                        } else if (job == "add" && result["result"] == "ok") {
                            popup("success", gettext("Choice saved successfully!"), gettext("Choice saved!"), 1500);
                        } else if (job == "voteAdd" && result["result"] == "added") {
                            choice_id.text(result["vote_count"]);
                            popup("success", gettext("Vote added successfully!\nVote count:") + result["vote_count"], gettext("Vote Added!"), 1500);
                        } else if (job == "voteRem" && result["result"] == "removed") {
                            choice_id.text(result["vote_count"]);
                            popup("success", gettext("Vote removed successfully!\nVote count:") + result["vote_count"], gettext("Vote Removed!"), 1500);
                        } else if (job == "voteRem" && result["result"] == "not_added") {
                            choice_id.text(result["vote_count"]);
                            popup("warning", gettext("No Choice found in db!"), gettext("Choice not Found!"));
                        } else if (job == "voteRem" && result["result"] == "no_votes") {
                            choice_id.text(result["vote_count"]);
                            popup("warning", gettext("No Votes Found!"), gettext("No Votes!"));
                        } else if (job == "getChoices" && result["result"] == "all_choices_failed") {
                            popup("warning", gettext("No Choices Found in db!"), gettext("Empty Response!"));
                        } else if (job == "getChoices" && result["result"] == "all_choices") {
                            if (question_id == result["question_id"]) {
                                setChoices(result["choices"], 'update');
                            } else {
                                question_id = result["question_id"];
                                $('#question_single').val(result["question_txt"]);
                                setChoices(result["choices"], 'set');
                            }
                        }
                    },
                    "complete": function () {
                    },
                    "error": function (xhr, textStatus, thrownError) {
                        popup("error", gettext("post Error:") + thrownError + " txtStatus:" + textStatus + " xhr:" + xhr, gettext("ajax post handler"));
                    },
                    "async": false
                });
            }

            if (job == "del" && no_confirm == false) {
                swal({
                    title: gettext("Are you sure?"),
                    text: gettext("You will not be able to recover this choice!"),
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: gettext("Yes, delete it!"),
                    cancelButtonText: gettext("No, cancel !"),
                    closeOnConfirm: false,
                    closeOnCancel: false
                }, function (isConfirm) {
                    if (isConfirm) {
                        do_post();
                        popup("success", gettext("Choice has been deleted."), gettext("deleted"), 1000);
                    } else {
                        swal(gettext("Cancelled"), gettext("Choice not deleted"), "error");
                    }
                });
            } else {
                do_post();
            }
        } else {
            swal({
                title: gettext("ajax post handler"),
                text: gettext("error in POST - Refreshing"),
                type: "error",
                confirmButtonText: "ok",
                timer: 5000
            });
            location.reload();
        }
        reloadJavascript();
    }

    /*Initial add click events to template*/
    $('.remVote').click(voteRemove);
    $('.addVote').click(voteAdd);
    reloadJavascript();
    save_start_status();

    /*TEMPORARY ARRAY FOR EDITED VALUES*/
    function notSavedTemp(item) {
        var choice_id = item[0];
        var choice_text = item[1];
        try {
            if (edited_unsaved[choice_id].length > 0) {
                edited_unsaved[choice_id][1] = choice_text;
            }
        } catch (err) {
            edited_unsaved[choice_id] = [];
            edited_unsaved[choice_id].push(start_values[choice_id][0]);
        }
    }

    /*SAVE START VALUES OF CHOICES*/
    function save_start_status() {
        $('#choice_table tr td label').each(function () {
            var choice_id = $(this).attr('for');
            var choice_text = $(this).text();
            if (choice_id != undefined) {
                start_values[choice_id] = [];
                start_values[choice_id].push(choice_text);
            }
        });
    }

    /*SAVE ROW AFTER EDITION*/
    function saveChanges(current_row_txt, current_row_id) {
        ajaxPoster("delete", edited_unsaved[current_row_id][0]);
        ajaxPoster("add", current_row_txt.trim());
        edited_unsaved[current_row_id][0] = current_row_txt;
    }

    /*ROW DELETE EVENT*/
    function DeleteRow() {
        var choice_text = $(this).parents('tr').first().children('td:nth-child(1)').children('input').val();
        rowRemover(choice_text);
        $(this).parents('tr').first().remove();
    }

    /*VOTE + EVENT*/
    function voteAdd() {
        var choice_text = $(this).parents('tr').first().children('td:nth-child(1)').children('input').val();
        var choice_id = $(this).parents('tr').first().children('td:nth-child(2)').children('div').first().children('label').first();
        ajaxPoster("voteAdd", choice_text.trim(), choice_id);
    }

    /*VOTE - EVENT*/
    function voteRemove() {
        var choice_text = $(this).parents('tr').first().children('td:nth-child(1)').children('input').val();
        var choice_id = $(this).parents('tr').first().children('td:nth-child(2)').children('div').first().children('label').first();
        ajaxPoster("voteRem", choice_text.trim(), choice_id);
    }

    /*REMOVE ROW*/
    function rowRemover(choice_text) {
        ajaxPoster("del", choice_text.trim());
    }

    /*ADD ROW*/
    function addRow(request_value, votes_count, edited) {
        $("#ajax_test_in").val("");
        var new_row = "";
        var start_vote_value;
        if (votes_count)
            start_vote_value = votes_count;
        else
            start_vote_value = "0";
        var table = $("#choice_table").children();
        var count = parseInt($('#choice_table tr').length) - 1;
        var next_choice_id = count.toString();
        var plus_minus = ["#plus_" + next_choice_id, "#minus_" + next_choice_id];
        if (edited)
            new_row = '<tr class="rowEditedNS"><td><label for="choice_' + next_choice_id + '" class="pull-left">';
        else
            new_row = '<tr><td><label for="choice_' + next_choice_id + '" class="pull-left">';
        new_row += request_value + '</label>';
        new_row += '<input id="choice_' + next_choice_id + '" class="clickedit tableWrapper" type="text" value="';
        new_row += request_value + '" style="display: none;"/></td><td>';
        new_row += '<div id="plus_' + next_choice_id + '" class="small-padding btn btn-info"><button class="widther-txt addVote btn-info"> + </button>';
        new_row += '<label class="no-padding" id="votes_' + next_choice_id + '"> ' + start_vote_value + ' </label>';
        new_row += '<button id="minus_' + next_choice_id + '"  class="widther-txt remVote btn-info"> - </button></div> ';
        if (edited)
            new_row += '<button class="rowEdit btn btn-lg btn-success">save!</button> ';
        else
            new_row += '<button class="rowEdit btn btn-primary">edit</button> ';
        new_row += '<button class="rowDelete btn btn-danger">delete</button></td></tr>';
        table.append(new_row);
        $(plus_minus[0]).click(voteAdd);
        $(plus_minus[1]).click(voteRemove);
    }

    /*ADD ROW POST*/
    $("#ajax_add").click(function (e) {
        e.preventDefault();
        var request_value = document.getElementById("ajax_test_in").value;
        try {
            if (request_value.trim().length < 2) {
                popup("warning", gettext("Minimum number of characters for a Choice is 2!"), gettext("Choice to short!"));
            } else {
                ajaxPoster("add", request_value.trim());
                ajaxPoster("getChoices", question_id);
                $(function () {
                    outliner('add');
                });
            }
        } catch (err) {
            popup("warning", gettext("Minimum number of characters for a Choice is 2!"), gettext("Choice to short!"));
        }
    });

    /*ROW EDITION HANDLERS*/
    function EditRow() {
        var this_input = $(this).parents('tr').first().children('td').first();
        var this_button = $(this).parents('tr').first().children('td:nth-child(2)').children('button:nth-child(2)');
        if (this_button.hasClass("btn-success")) {
            this_button.removeClass("btn-success btn-lg");
            this_button.removeClass("rowEdit");

            if (dark())
                this_button.addClass("btn-primary-outline");
            else
                this_button.addClass("btn-primary");
            popup("success", gettext("Choice changes saved to db!"), gettext("Saved Successfully!"), 1200);
            this_button.text(gettext("Saved"));
            $(this).parents('tr').removeClass("rowEditedNS");
            var current_row_txt = this_input.children('input').val();
            var current_row_id = this_input.children('input').attr('id');
            saveChanges(current_row_txt, current_row_id);
        } else {
            this_input.children('label').hide();
            this_input.children('input').show().focus();
        }
    }

    /*ROW EDITION CLICK EVENT*/
    function rowEditable() {
        $('.clickedit').hide()
            .focusout(endEdit)
            .keyup(function (e) {
                var this_button = $(this).parents('tr').first().children('td:nth-child(2)').children('button:nth-child(2)');
                if (dark())
                    this_button.removeClass("btn-primary-outline");
                else
                    this_button.removeClass("btn-primary");
                this_button.addClass("btn-success btn-lg");
                this_button.addClass("rowEdit");
                this_button.text(gettext("save !"));
                $(this).parents('tr').addClass("rowEditedNS");
                var temp_txt = $(this).parents('tr').first().children('td:nth-child(1)').children('input').val();
                var temp_id = $(this).parents('tr').first().children('td:nth-child(1)').children('input').attr('id');
                notSavedTemp([temp_id, temp_txt]);

                if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
                    endEdit(e);
                    return false;
                } else {
                    return true;
                }
            })
            .prev().click(function () {
                var temp_txt = $(this).parents('tr').first().children('td:nth-child(1)').children('input').val();
                var temp_id = $(this).parents('tr').first().children('td:nth-child(1)').children('input').attr('id');
                notSavedTemp([temp_id, temp_txt]);
                $(this).hide();
                $(this).next().show().focus();
            });
    }

    /* AFTER ROW EDITION HANDLER*/
    function endEdit(e) {
        var input = $(e.target),
            label = input && input.prev();
        label.text(input.val());
        input.hide();
        label.show();
    }

    /*STYLED POPUP PLUGIN -sweetalert- */
    function popup(type, txt, title, timer) {
        if (timer)
            swal({title: title, text: txt, type: type, timer: timer, showConfirmButton: false});
        else
            swal({title: title, text: txt, type: type, confirmButtonText: "ok"});
    }

    /*QUESTION CHANGED RECEIVED CHOICES HANDLER*/
    function setChoices(input, job) {
        $('#choice_table').children('tbody').children('tr').slice(1).remove();
        var choice_array = input.split('\n');
        var choice_vote;
        var i;
        var boolean_flag;
        if (job == 'update') {
            for (i = 0; i < choice_array.length - 1; i++) {
                choice_vote = choice_array[i].split(';');
                try {
                    boolean_flag = true;
                    for (var key in edited_unsaved) {
                        var obj = edited_unsaved[key];
                        if (obj[0].trim() == choice_vote[0].trim()) {
                            addRow(obj[1], choice_vote[1], true);
                            boolean_flag = false;
                        }
                    }
                    if (boolean_flag) {
                        addRow(choice_vote[0], choice_vote[1], false);
                    }
                } catch (err) {
                    addRow(choice_vote[0], choice_vote[1], false);
                }
            }
        } else {
            for (i = 0; i < choice_array.length - 1; i++) {
                choice_vote = choice_array[i].split(';');
                addRow(choice_vote[0], choice_vote[1], false);
            }
            popup("success", gettext("Question changed successfully!\nCurrent Question ID:") + question_id, gettext("Question changed!"), 1500);
        }
    }

    /*QUESTION LIST DROPDOWN CHANGE HANDLER*/
    dropdown.change(function () {
        var dropdown_value = this.value;
        ajaxPoster("getChoices", dropdown_value);
        $(function () {
            outliner('add');
        });

    });

    function show_question() {
        question.removeClass("no_display").addClass("yes_display");
        dropdown.removeClass("yes_display").addClass("no_display");
    }

    function show_dropdown() {
        question.removeClass("yes_display").addClass("no_display");
        dropdown.removeClass("no_display").addClass("yes_display");
    }

    /*QUESTION BUTTON*/
    $("#question_button").click(function (e) {
        e.preventDefault();
        if (save_btn.hasClass('btn-success'))
            popup("warning", gettext("Save currently edited Question to show dropdown list!"), gettext("Question not saved"));
        else
            show_dropdown();
    });

    /*SAVE QUESTION BUTTON CONFIRMATION*/
    var confirm_save_main = false;

    save_btn.on('click', function (e) {
        if (question.hasClass("no_display"))
            show_question();
        if (confirm_save_main === true) {
            confirm_save_main = false;
            return;
        }
        e.preventDefault();
        if (save_btn.hasClass("btn-success")) {
            var question_edited_txt = question.val();
            if (question_edited_txt.trim().length < 2) {
                popup("warning", gettext("Minimum number of characters for a Question is 2!"), gettext("Question to short!"));
            } else {
                ajaxPoster("questionUpdate", question_edited_txt);
                swal({
                        title: gettext("Question saved!"),
                        text: gettext("What do you want to do now?"),
                        type: "success",
                        showCancelButton: true,
                        confirmButtonColor: "#5BBFDD",
                        confirmButtonText: gettext("go to home page"),
                        cancelButtonText: gettext("continue edition"),
                        closeOnConfirm: false,
                        closeOnCancel: true
                    },
                    function (isConfirm) {
                        if (isConfirm) {
                            confirm_save_main = true;
                            save_btn.trigger('click');
                        }
                        else {
                            if (dark())
                                save_btn.removeClass("btn-success").addClass("btn-primary-outline");
                            else
                                save_btn.removeClass("btn-success").addClass("btn-primary");
                            question.removeClass("edited");
                            save_btn.val(gettext("edit question"));
                        }
                    });
            }
        } else {
            question.focus();
        }
    });

    /*ADMIN COMMENT EVENT*/



    function first_row_edition_event() {
        question.keyup(function (e) {
            question.addClass('edited');
            if (dark())
                save_btn.removeClass("btn-primary-outline").addClass("btn-success").val(gettext("save question"));
            else
                save_btn.removeClass("btn-primary").addClass("btn-success").val(gettext("save question"));
            if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13))
                return false;
            else
                return true;
        })
            .prev().click(function () {
                $(this).next().show().focus();
            });
    }


    /*SECURITY TOKEN HANDLING*/
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
});