<!--
 * @Author: Jerryk jerry@icewhale.org
 * @Date: 2022-08-03 15:28:43
 * @LastEditors: zhanghengxin ezreal.zhang@icewhale.org
 * @LastEditTime: 2023-07-13 17:02:12
 * @FilePath: /CasaOS-UI/main/src/components/filebrowser/modals/NewNetworkStorage.vue
 * @Description:
 *
 * Copyright (c) 2022 by IceWhale, All Rights Reserved.
-->
<template>
	<div class="modal-card">
		<!-- Modal-Card Header Start -->
		<header class="modal-card-head">
			<div class="is-flex-grow-1">
				<h3 class="title is-3">{{ $t('Connect Network Storage') }}</h3>
			</div>
			<div>
				<button class="delete" type="button" @click="$emit('close')"/>
			</div>
		</header>
		<!-- Modal-Card Header End -->

		<!-- Modal-Card Body Start -->
		<section class="modal-card-body ">
			<div class="node-card">
				<div class=" mt-5 mb-5">
					<b-field :label="$t('Server Address')">
						<b-autocomplete ref="inputs" v-model="host" :data="filteredDataObj"
										:placeholder="$t('eg : smb://192.168.1.1')"
										append-to-body field="host" max-height="120px" open-on-focus
										@select="option => selected = option">
							<template slot-scope="props">
								<div class="media is-align-items-center smb-media">
									<div class="media-left is-flex is-align-items-center">
										<b-icon icon="history"></b-icon>
									</div>
									<div class="media-content">
										{{ props.option.host }}

									</div>
								</div>
							</template>

						</b-autocomplete>

					</b-field>
					<div class="message-alert is-flex is-align-items-center">
						<div class="left mr-2 is-flex is-align-items-center">
							<b-icon icon="danger" pack="casa"></b-icon>
						</div>
						<div class="main is-flex is-align-items-center">
							{{ $t('Support Samba Address eg : smb://192.168.1.1') }}
						</div>
					</div>

					<div class="field is-flex ">
						<label class="label is-flex-grow-1">{{ $t('Connect As Guest') }}</label>
						<b-switch v-model="isGuest" type="is-dark"></b-switch>
					</div>

					<div v-if="!isGuest" class="mt-5">
						<b-field :label="$t('Name')" class="mb-5" horizontal>
							<b-input v-model="username" expanded name="username" @blur="checkout"></b-input>
						</b-field>
						<b-field :label="$t('Password')" class="mb-5" horizontal>
							<b-input v-model="password" expanded name="password" type="password"
									 @blur="checkout"></b-input>
						</b-field>
					</div>

				</div>

			</div>

		</section>
		<!-- Modal-Card Body End -->
		<!-- Modal-Card Footer Start-->
		<footer class="modal-card-foot is-flex is-align-items-center">
			<div class="is-flex-grow-1"></div>
			<div>
				<b-button :disabled="risk" :label="$t('Connect')" :loading="isConnecting" expaned rounded
						  type="is-primary"
						  @click="connect"/>
			</div>
		</footer>
		<!-- Modal-Card Footer End -->
	</div>
</template>

<script>
import smoothReflow from 'vue-smooth-reflow'
import events       from '@/events/events';

export default {
	mixins: [smoothReflow],
	props: {
		item: {
			type: Object,
			default: () => ({})
		},
	},
	data() {
		return {
			isGuest: true,
			isConnecting: false,
			host: "",
			username: "",
			password: "",
			selected: null,
			risk: false,
			data: [
				{
					host: 'smb://192.168.1.1',
					username: '',
					password: '',
				},
				{
					host: 'smb://192.168.1.2',
					username: 'root',
					password: 'password',
				},
				{
					host: 'smb://192.168.1.3',
					username: '',
					password: '',
				},
				{
					host: 'smb://192.168.1.4',
					username: '',
					password: '',
				}
			]
		}
	},
	computed: {
		filteredDataObj() {
			return this.$store.state.networkStorage
		}
	},
	watch: {
		selected(val) {
			this.isGuest = val.guest
			if (!val.guest) {
				this.username = val.username
				this.password = val.password
			}
		}
	},
	created() {

	},
	mounted() {
		//Smooth
		this.$smoothReflow({
			el: '.modal-card',
			property: ['height', 'width'],
			transition: 'height .25s ease, width .75s ease-out'
		})

		setTimeout(() => {
			this.$refs.inputs.focus()
		}, 500)

	},
	methods: {
		connect() {
			if (this.host.startsWith("smb://") || this.host.startsWith("nfs://")) {
				if (!this.isGuest && (this.username == "" || this.password == "")) {
					this.$buefy.toast.open({
						message: this.$t(`Username or password cannot be empty.`),
						type: 'is-danger'
					})

				} else {

					const host = this.host.replace("smb://", "").replace("nfs://", "")
					const data = this.isGuest ? {
						host: host,
						username: "guest",
						password: "guest"
					} : {
						host: host,
						username: this.username,
						password: this.password
					}
					this.isConnecting = true
					this.$api.samba.createConnection(data).then(res => {
						this.isConnecting = false
						this.saveNewLoginInfoToLocalStorage()
						this.$EventBus.$emit(events.RELOAD_MOUNT_LIST);
						const item = {
							path: res.data.data.mount_point
						}
						this.$EventBus.$emit(events.GOTO, item);
						this.$emit('close')
					}).catch(err => {
						this.isConnecting = false
						this.$buefy.toast.open({
							message: this.$t(err.response.data.data || err.response.data.message),
							type: 'is-danger'
						})
					})


				}

			} else {
				this.$buefy.toast.open({
					message: this.$t(`Please enter a correct Samba address!`),
					type: 'is-danger'
				})

			}
		},

		saveNewLoginInfoToLocalStorage() {
			let oldInfo = this.$store.state.networkStorage
			const loginItem = this.isGuest ? {
				host: this.host,
				guest: true,
				username: "",
				password: "",
			} : {
				host: this.host,
				guest: false,
				username: this.username,
				password: "",
			}
			const isInArray = oldInfo.some(item => item.host === loginItem.host && item.guest === loginItem.guest)
			if (!isInArray) {
				oldInfo.push(loginItem)
				this.$store.commit('SET_NETWORK_STORAGE', oldInfo)
			}
		},

		checkout(e) {
			if (/[^a-zA-Z0-9@#*.]/g.test(e.target.value)) {
				this.risk = true
				this.$buefy.toast.open({
					message: `Special characters may cause security problems`,
					type: 'is-danger'
				})
				console.error(`Special characters may cause security problems`)
			} else {
				this.risk = false
			}
		}
	},
}
</script>

<style lang="scss" scoped>
.modal-card {
	max-width: 40rem;
}

.modal-card-body {
	overflow-y: hidden;
}

.message-alert {
	padding: 0.4rem 1rem;
	margin-bottom: 1.75rem;
	background: #fff7e6;
	border-radius: 4px;
	color: #d99000;
	font-size: 0.875rem;
}
</style>

<style lang="scss">
.network-storage-modal {
	.field-label {
		text-align: left;
	}
}

.smb-media {
	color: #999;
}
</style>